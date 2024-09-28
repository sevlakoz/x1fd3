import numpy as np
import numpy.typing as npt
from scipy.interpolate import splrep, splev   # type: ignore

from .parameters import Parameters
from .logger import Logger
from .an_pec import AnPec

Float64Array = npt.NDArray[np.float64]

class PWCurve:
    '''
    class for point-wise curve
    '''
    def __init__(
        self,
        fname: str = ''
    ) -> None:
        '''
        init = read data if file provided 
        '''
        self.npoint = 0

        self.rval: Float64Array = np.array([])
        self.cval: Float64Array = np.array([])
        self.eval: Float64Array = np.array([])

        if fname:
            self.read_file(fname)

    def read_file(
        self,
        fname: str
    ) -> None:
        '''
        read points from file
        '''
        data = np.loadtxt(fname).T

        ncol = len(data)

        if ncol == 2:
            self.rval = data[0]
            self.cval = data[1]
            self.eval = np.maximum(
                np.full(len(data[1]), 100.),
                data[1] / 100.
            )
        elif ncol == 3:
            self.rval = data[0]
            self.cval = data[1]
            self.eval = data[2]
        else:
            raise RuntimeError(f'found {ncol} columns in {fname}, only 2 or 3 supported')

        self.npoint = len(self.rval)

    def spline(
        self,
        r_grid: Float64Array
    ) -> Float64Array:
        '''
        cubic spline with range check
        '''
        rng_inp = [r_grid[0], r_grid[-1]]
        rng_self = [self.rval[0], self.rval[-1]]
        if rng_inp[0] < rng_self[0] or rng_inp[-1] > rng_self[-1]:
            raise RuntimeError(f'grid for spline out of range - {rng_inp} not in {rng_self}')

        spl_pec = splrep(self.rval, self.cval)
        c_grid: npt.NDArray[np.float_] = splev(r_grid, spl_pec)   # type: ignore
        return c_grid

    def print_with_anpec(
        self,
        params: Parameters,
        out: Logger
    ) -> None:
        '''
        print point-wise and approximated pec
        '''
        # pec calc
        pec_an = AnPec(params).calc(self.rval)

        # print with loop over r
        lbl = f'U({params["ptype"]}),cm-1'
        out.print(f'{"R,A":>10}{"U(p-w),cm-1":>20}{lbl:>20}{"delta,cm-1":>20}')
        for r_inp, u_inp, u_cal in zip(self.rval, self.cval, pec_an):
            out.print(f'{r_inp:10.5f}{u_inp:20.3f}{u_cal:20.3f}{u_inp - u_cal:20.3f}')
