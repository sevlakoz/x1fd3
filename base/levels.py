from typing import Dict
import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh_tridiagonal     # type: ignore

from .p_w_curve import PWCurve
from .parameters import Parameters
from .emo import emo

class Levels:
    '''
    class for vib-rot level
    '''
    def __init__(
        self,
        ptype: str,
        params: Parameters,
        pec: PWCurve = PWCurve()
    ) -> None:
        '''
        init = calculate vib-rot levels for given set of parameters / point-wise pec
        '''
        self.energy: Dict[int, Dict[int, float]] = {}
        self.rot_const: Dict[int, Dict[int, float]] = {}
        self.wavef_grid: Dict[int, Dict[int, npt.NDArray[np.float64]]] = {}
        self.r_grid: npt.NDArray[np.float64] = np.array([])

        # physical constants
        au_to_da = 5.48579909065e-4
        au_to_cm = 219474.63067
        a0_to_ang = 0.529177210903

        # grid point number
        ngrid = 50000

        # reduced mass
        mu = params['mass1'] * params['mass2'] / (params['mass1'] + params['mass2'])

        # h^2 / (2*mu) [cm-1 * A^2]
        scale = au_to_da * au_to_cm * a0_to_ang**2 / (2 * mu)

        # grid
        step = (params['rmax'] - params['rmin']) / (ngrid - 1)
        r_grid = np.linspace(params['rmin'], params['rmax'], ngrid)

        if ptype == 'pw':
            # cubic spline for pec
            u_grid = pec.spline(r_grid)
            emax = u_grid[-1]
        elif ptype == 'an':
            # analytic: EMO
            an_ptype = params['ptype']
            if an_ptype == 'EMO':
                u_grid = emo(r_grid, params)
                emax = params['de']
            else:
                raise RuntimeError(f'ERROR: Uknown analytic pec type "{an_ptype}"')
        else:
            raise RuntimeError(f'ERROR: Uknown pec type "{ptype}"')

        # loop over J to calculate level energies

        for j in range(params['jmax'] + 1):

            # diagonal elements (ngrid)
            diagonal = u_grid / scale + j * (j + 1) / r_grid**2 + 2 * step**-2

            # off-diagonal elements (ngrid-1)
            off_diag = np.full(ngrid - 1, -step**-2)

            # SciPy routine to calculate eigenvalues and eigenvectors
            results = eigh_tridiagonal(
                diagonal,
                off_diag,
                select = 'v',
                select_range = (0., emax / scale)
            )

            self.energy[j] = {}
            self.rot_const[j] = {}
            self.wavef_grid[j] = {}

            for v, en in enumerate(results[0]):
                wf = results[1][:, v]

                # correction for fd3 scheme
                fd_cor = step**2 / scale / 12 * np.sum(
                    (wf * (u_grid - en * scale))**2
                )

                self.energy[j][v] = en * scale + fd_cor
                self.rot_const[j][v] = scale * np.sum(wf**2 / r_grid**2)
                self.wavef_grid[j][v] = wf
        self.r_grid = r_grid

    def print(
        self,
    ) -> None:
        '''
        print vib-rot levels from dict in custom format
        '''
        print('\n=== Energy levels ===')
        for j, en_jv in self.energy.items():
            print(f'\nJ = {j}\n{"v":>3}{"E,cm-1":>15}{"Bv,cm-1":>15}')
            for v, en_v in en_jv.items():
                print(f'{v:3d}{en_v:15.5f}{self.rot_const[j][v]:15.8f}')

    def print_with_expdata(
        self,
        expdata: Dict[int, Dict[int, float]]
    ) -> None:
        '''
        print cal and exp vib-rot levels in custom format
        '''
        print(f'\n{"J":>4}{"v":>4}{"Eexp,cm-1":>15}{"Ecalc,cm-1":>15}{"delta,cm-1":>15}')
        for j, en_jv in self.energy.items():
            for v, en_cal in en_jv.items():
                if j in expdata:
                    if v in expdata[j]:
                        en_exp = expdata[j][v]
                        print(f'{j:4d}{v:4d}{en_exp:15.5f}{en_cal:15.5f}{en_exp - en_cal:15.5f}')
        print()
