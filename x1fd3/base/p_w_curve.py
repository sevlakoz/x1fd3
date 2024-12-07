import numpy as np
import numpy.typing as npt
from scipy.interpolate import CubicSpline   # type: ignore

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
        fname:str='',
        rvs:Float64Array=np.array([]),
        cvs:Float64Array=np.array([]),
        evs:Float64Array=np.array([])
    ) -> None:
        '''
        init = read data if file provided 
        '''
        self.npoint = 0

        self.rvs:Float64Array = np.array([])
        self.cvs:Float64Array = np.array([])
        self.evs:Float64Array = np.array([])

        arr_check = len(rvs) * len(cvs)

        if fname and arr_check:
            raise RuntimeError('ambiguous init, exiting')

        if fname:
            self.read_file(fname)

        if arr_check:
            self.set_arrays(rvs, cvs, evs)

    def read_file(
        self,
        fname:str
    ) -> None:
        '''
        read points from file
        '''
        data = np.loadtxt(fname).T

        ncol = len(data)

        if ncol == 2:
            self.rvs = data[0]
            self.cvs = data[1]
            self.evs = np.maximum(
                np.full(len(data[1]), 100.),
                data[1] / 100.
            )
        elif ncol == 3:
            self.rvs = data[0]
            self.cvs = data[1]
            self.evs = data[2]
        else:
            raise RuntimeError(f'found {ncol} columns in {fname}, only 2 or 3 supported')

        self.npoint = len(self.rvs)

    def set_arrays(
        self,
        rvs:Float64Array,
        cvs:Float64Array,
        evs:Float64Array
    ) -> None:
        '''
        set r, c, e arrays directly
        '''
        lr = len(rvs)
        lc = len(cvs)
        le = len(evs)
        if lr != lc or le not in [0, lc]:
            raise RuntimeError('arrays must be same size')
        self.rvs = rvs
        self.cvs = cvs
        if le != 0:
            self.evs = evs
        else:
            self.evs = np.full(lc, 100.)

    def spline(
        self,
        r_grid:Float64Array
    ) -> Float64Array:
        '''
        cubic spline with range check
        '''
        rng_inp = [r_grid[0], r_grid[-1]]
        rng_self = [self.rvs[0], self.rvs[-1]]
        if rng_inp[0] < rng_self[0] or rng_inp[-1] > rng_self[-1]:
            raise RuntimeError(f'grid for spline out of range - {rng_inp} not in {rng_self}')

        spl_pec = CubicSpline(self.rvs, self.cvs)
        c_grid:npt.NDArray[np.float_] = spl_pec(r_grid)   # type: ignore
        return c_grid

    def print_with_anpec(
        self,
        params:Parameters,
        out:Logger
    ) -> None:
        '''
        print point-wise and approximated pec
        '''
        # pec calc
        pec_an = AnPec(params).calc(self.rvs)

        # print with loop over r
        lbl = f'U({params["ptype"]}),cm-1'
        out.print(f'{"R,A":>10}{"U(p-w),cm-1":>20}{lbl:>20}{"delta,cm-1":>20}')
        for r_inp, u_inp, u_cal in zip(self.rvs, self.cvs, pec_an):
            out.print(f'{r_inp:10.5f}{u_inp:20.3f}{u_cal:20.3f}{u_inp - u_cal:20.3f}')
