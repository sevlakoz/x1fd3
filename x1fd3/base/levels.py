from typing import ClassVar, Any
import numpy as np
import numpy.typing as npt
from scipy.linalg import eigh_tridiagonal     # type: ignore

from .p_w_curve import PWCurve
from .parameters import Parameters
from .an_pec import AnPec
from .logger import Logger
from .exp_data import ExpData

Float64Array = npt.NDArray[np.float64]

class Levels:
    '''
    class for vib-rot level
    '''
    # physical constants
    AU_TO_DA:ClassVar[float] = 5.48579909065e-4
    AU_TO_CM:ClassVar[float] = 219474.63067
    A0_TO_ANG:ClassVar[float] = 0.529177210903
    # grid step
    STEP:ClassVar[float] = 1e-4

    def __init__(
        self,
        params:Parameters,
        pec:PWCurve,
        expdata:ExpData
    ) -> None:
        '''
        init = calculate vib-rot levels for given set of parameters / point-wise pec
        '''
        # save exp levels
        self.energy_exp = expdata.energy
        self.nlev_exp = expdata.nlev

        # empty vars for calc levels
        self.energy:dict[int, dict[int, float]] = {}
        self.rot_const:dict[int, dict[int, float]] = {}
        self.wavef_grid:dict[int, dict[int, Float64Array]] = {}
        self.r_grid:Float64Array = np.array([])

        # reduced mass
        mu = params['mass1'] * params['mass2'] / (params['mass1'] + params['mass2'])

        # h^2 / (2*mu) [cm-1 * A^2]
        scale = self.AU_TO_DA * self.AU_TO_CM * self.A0_TO_ANG**2 / (2 * mu)

        # grid
        step = self.STEP
        r_grid = np.arange(params['rmin'], params['rmax'] + step / 2, step)
        n_grid = r_grid.size
        if n_grid < 1000:
            raise RuntimeError('range ["rmin", "rmax"] seems to be too small')

        if pec.npoint > 0:
            # cubic spline for pw pec
            u_grid = pec.spline(r_grid)
            emax = u_grid[-1] / scale
        else:
            # analytic
            if 'ptype' in params.keys():
                u_grid = AnPec(params).calc(r_grid)
                if params['ptype'] in ('EMO', 'MLR', 'DELR'):
                    emax = params['de'] / scale
                else:
                    raise RuntimeError(f'cant calculate energy range for \"{params["ptype"]}\"')
            else:
                raise RuntimeError('"ptype" not in Parameters.keys()')

        # J and eigenvalues search ranges
        select_range:dict[int, tuple[Any, Any]] = {}
        if self.nlev_exp > 0:
            jrange = self.energy_exp.keys()
            select = 'i'
            for j in jrange:
                select_range[j] = (
                    min(self.energy_exp[j].keys()),
                    max(self.energy_exp[j].keys())
                )
        else:
            jrange = range(params['jmax'] + 1) #type: ignore
            select = 'v'

        # loop over J to calculate level energies
        for j in jrange:
            # diagonal elements (ngrid)
            diagonal = u_grid / scale + j * (j + 1) * r_grid**-2 + 2 * step**-2

            # off-diagonal elements (ngrid-1)
            off_diag = np.full(n_grid - 1, -step**-2)

            # SciPy routine to calculate eigenvalues and eigenvectors
            results = eigh_tridiagonal(
                diagonal,
                off_diag,
                select=select,
                select_range=select_range.get(j, (0., emax))
            )

            # dicts for results
            self.energy[j] = {}
            self.rot_const[j] = {}
            self.wavef_grid[j] = {}

            # calc correction for E(v,J) and store results
            for v, en in enumerate(results[0]):
                wf = results[1][:, v]
                # correction for fd3 scheme
                fd_cor = step**2 / scale / 12 * np.sum(
                    (wf * (u_grid - en * scale))**2
                )

                # E, Bv, WF
                self.energy[j][v] = en * scale + fd_cor
                self.rot_const[j][v] = scale * np.sum(wf**2 * r_grid**-2)
                self.wavef_grid[j][v] = wf

        # grid for R
        self.r_grid = r_grid

    def print(
        self,
        out:Logger
    ) -> None:
        '''
        print vib-rot levels from dict in custom format
        '''
        out.print('\n=== Energy levels ===')
        for j, en_jv in self.energy.items():
            out.print(f'\nJ = {j}\n{"v":>3}{"E,cm-1":>15}{"Bv,cm-1":>15}')
            for v, en_v in en_jv.items():
                out.print(f'{v:3d}{en_v:15.3f}{self.rot_const[j][v]:15.5f}')

    def print_with_expdata(
        self,
        out:Logger
    ) -> None:
        '''
        print cal and exp vib-rot levels in custom format
        '''
        if self.nlev_exp > 0:
            out.print(f'\n{"J":>4}{"v":>4}{"Eexp,cm-1":>15}{"Ecalc,cm-1":>15}{"delta,cm-1":>15}')
            for j, en_jv in self.energy.items():
                for v, en_cal in en_jv.items():
                    en_exp = self.energy_exp[j][v]
                    out.print(f'{j:4d}{v:4d}{en_exp:15.3f}{en_cal:15.3f}{en_exp - en_cal:15.3f}')
            out.print()
        else:
            raise RuntimeError('No experimental levels provided')
