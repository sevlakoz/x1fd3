import numpy as np
import numpy.typing as npt
from scipy.interpolate import splrep, splev   # type: ignore

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
        self.rval: npt.NDArray[np.float64] = np.array([])
        self.cval: npt.NDArray[np.float64] = np.array([])

        if fname:
            self.read_file(fname)

    def read_file(
        self,
        fname: str
    ) -> None:
        '''
        read points from file
        '''
        tmp_rval = []
        tmp_cval = []

        with open(fname, encoding = 'utf-8') as inp:
            for line in inp:
                if line.lstrip() == '' or line.lstrip()[0] == '#':
                    continue
                line = line.split()   # type: ignore
                tmp_rval.append(float(line[0]))
                tmp_cval.append(float(line[1]))

        self.rval = np.array(tmp_rval)
        self.cval = np.array(tmp_cval)

    def spline(
        self,
        r_grid: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
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
