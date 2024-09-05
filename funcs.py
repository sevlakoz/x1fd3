import os
import sys
from configparser import ConfigParser
from typing import Dict, Any, List, Tuple
import numpy as np
import numpy.typing as npt
from scipy.optimize import least_squares      # type: ignore
from scipy.interpolate import splrep, splev   # type: ignore
from scipy.linalg import eigh_tridiagonal     # type: ignore

#=======================================================================
#=======================================================================

class PWcurve:
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
        self.rval: List[float] = []
        self.cval: List[float] = []

        if fname:
            self.read_file(fname)

    def read_file(
        self,
        fname: str
    ) -> None:
        '''
        read points from file
        '''
        self.rval = []
        self.cval = []

        with open(fname, encoding = 'utf-8') as inp:
            for line in inp:
                if line.lstrip() == '' or line.lstrip()[0] == '#':
                    continue
                line = line.split()   # type: ignore
                self.rval.append(float(line[0]))
                self.cval.append(float(line[1]))

        self.rval = np.array(self.rval)   # type: ignore
        self.cval = np.array(self.cval)   # type: ignore

    def spline(
        self,
        r_grid: npt.NDArray[np.float64]
    ) -> npt.NDArray[np.float64]:
        '''
        cubic spline with range check
        '''
        if r_grid[0] < self.rval[0] or r_grid[-1] > self.rval[-1]:
            print(f'WARNING: grid for spline out of range - [{r_grid[0]}, {r_grid[-1]}] not in [{self.rval[0]}, {self.rval[-1]}]')
        spl_pec = splrep(self.rval, self.cval)
        c_grid: npt.NDArray[np.float_] = splev(r_grid, spl_pec)   # type: ignore
        return c_grid

#=======================================================================

class Levels:
    '''
    class for vib-rot level
    '''
    def __init__(
        self,
        ptype: str,
        params: Dict[str, Any],
        pec: PWcurve = PWcurve()
    ) -> None:
        '''
        init = calculate vib-rot levels for given set of parameters / point-wise pec
        '''
        self.energy: Dict[int, Dict[int, float]] = {}
        self.rot_const: Dict[int, Dict[int, float]] = {}
        self.wavef_grid: Dict[int, Dict[int, npt.NDArray[np.float64]]] = {}
        self.r_grid: npt.NDArray[np.float64] = np.array([])

        # physical constants
        au_to_Da = 5.48579909065e-4
        au_to_cm = 219474.63067
        a0_to_A = 0.529177210903

        # grid point number
        ngrid = 50000

        # reduced mass
        mu = params['mass1'] * params['mass2'] / (params['mass1'] + params['mass2'])

        # h^2 / (2*mu) [cm-1 * A^2]
        scale = au_to_Da * au_to_cm * a0_to_A**2 / (2 * mu)

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
                u_grid = np.array(
                    list(
                        map(lambda x: emo(x, params), r_grid)
                    )
                )
                emax = params['de']
            else:
                sys.exit(f'ERROR: Uknown analytic pec type "{an_ptype}"')
        else:
            sys.exit(f'ERROR: Uknown pec type "{ptype}"')

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
#=======================================================================

class MatrixElements:
    '''
    class for matrix elements
    '''
    def __init__(
        self,
        params: Dict[str, Any],
        levels: Levels,
        dm: PWcurve
    ) -> None:
        '''
        init = calculate matrix elements of given dipole function
        '''
        self.v1: int = params['v1']
        self.v2: int = params['v2']

        self.energy1: Dict[int, Dict[int, float]] = {}
        self.energy2: Dict[int, Dict[int, float]] = {}
        self.matrix_elements: Dict[int, Dict[int, np.float64]] = {}

        # cubic spline to find DM values
        d_grid = dm.spline(levels.r_grid)

        # matrix elements calc
        for j2 in levels.energy.keys():
            self.energy1[j2] = {}
            self.energy2[j2] = {}
            self.matrix_elements[j2] = {}
            for j1 in levels.energy.keys():
                self.energy1[j2][j1] = levels.energy[j1][self.v1]
                self.energy2[j2][j1] = levels.energy[j2][self.v2]
                self.matrix_elements[j2][j1] = np.sum(
                    levels.wavef_grid[j1][self.v1] *
                    levels.wavef_grid[j2][self.v2] *
                    d_grid
                )
    def print(
        self
    ) -> None:
        '''
        print calculated matrix elements in custom format
        '''
        print("\n=== Transition energies & Intergals <f(v',J')|d|f(v'',J'')>,D ===\n")
        print(f"v'' = {self.v1}")
        print(f"v'  = {self.v2}\n")

        for j2, me_j2j1 in self.matrix_elements.items():
            print(f"J' = {j2}")
            print(f'''{"J''":>4}{"E',cm-1":>15}{"E'',cm-1":>15}{"<f'|d|f''>,D":>15}''')
            for j1, me in me_j2j1.items():
                en2 = self.energy2[j2][j1]
                en1 = self.energy1[j2][j1]
                print(f"{j1:4d}{en2:15.5f}{en1:15.5f}{me:15.5e}")
            print()

    def _ht(
        self
    ) -> None:
        '''
        ht comp
        '''

        jm = max(self.matrix_elements.keys())

        jlist = []
        for j1 in range(jm, 0, -1):
            j2 = j1 - 1
            jlist.append((j2, j1))
        for j1 in range(jm):
            j2 = j1 + 1
            jlist.append((j2, j1))

        print("*  J' J''           freq             me        Sa            E''            pop            int        Se              A")
        for j2, j1 in jlist:
            dj = j2 - j1
            if dj == 1:
                lbl = "R"
                Sa = (j1 + 1) / (2 * j1 + 1)
                Se =  j2      / (2 * j2 + 1)
            elif dj == -1:
                lbl = "P"
                Sa = j1       / (2 * j1 + 1)
                Se = (j2 + 1) / (2 * j2 + 1)
            else:
                sys.exit('ERROR: wrong dJ')

            e2 = self.energy2[j2][j1]
            e1 = self.energy1[j2][j1]
            freq = e2 - e1
            me = self.matrix_elements[j2][j1]
            pop = (2 * j1 + 1) * np.exp(-e1 / 0.695 / 298.0)
            A = 3.137e-7 * me ** 2 * Se * freq ** 3
            inten = pop * me ** 2 * Sa
            print(f"{lbl}{j2:4d}{j1:4d}{freq:15.5f}{me:15.5e}{Sa:10.5f}{e1:15.5f}{pop:15.5e}{inten:15.5e}{Se:10.5f}{A:15.5e}")

#=======================================================================

class Parameters(dict):
    '''
    dict with custom methods for required parameters
    '''
    def read_pec_params(
            self,
            fname: str
        ) -> None:
        '''
        read params for PEC from file
        '''
        input_parser = ConfigParser(delimiters=(' ', '\t'))
        input_parser.read(fname)

        if len(input_parser.sections()) > 1:
            sys.exit(f'ERROR: Two or more analytic functions given in "{fname}"')

        ptype = input_parser.sections()[0]

        if not ptype in ['EMO']:
            sys.exit(f'ERROR:  Uknown potential type "{ptype}"')

        tmp = {}

        for keyword, value in input_parser[ptype].items():
            if keyword in ('q'):
                tmp[keyword] = int(value)
            elif keyword in ('re', 'de', 'rref'):
                tmp[keyword] = float(value)                              # type: ignore
            elif keyword in ('beta'):
                tmp[keyword] = np.array(list(map(float, value.split()))) # type: ignore

        params_check = {
            'EMO': set(['re', 'de', 'rref', 'q', 'beta'])
        }

        if set(tmp.keys()) != params_check[ptype]:
            sys.exit(f'ERROR:  for {ptype} the following parameters must be given: {params_check[ptype]}')

        self.update(tmp)
        self['ptype'] = ptype

    def read_vr_calc_params(
            self,
            fname: str,
            rtype: str
        ) -> None:
        '''
        read params for vib-rot level calculation from file
        '''
        if not rtype in ['ENERGY', 'SPECTRUM', 'FIT']:
            sys.exit(f'ERROR:  Uknown run type "{rtype}"')

        # read calc params
        input_parser = ConfigParser(delimiters=(' ', '\t'))
        input_parser.read(fname)

        if len(input_parser.sections()) > 1:
            sys.exit(f'ERROR: Two or more sets of parameters given in "{fname}"')

        if input_parser.sections()[0] != rtype:
            sys.exit(f'ERROR: run type in "{fname}" is not consistent with the actual run type')

        tmp = {}

        for keyword, value in input_parser[rtype].items():
            if keyword in ('jmax', 'v1', 'v2'):
                tmp[keyword] = int(value)
            elif keyword in ('mass1', 'mass2', 'rmin', 'rmax'):
                tmp[keyword] = float(value)                        # type: ignore

        params_check = {
            'ENERGY':   set(['mass1', 'mass2', 'rmin', 'rmax', 'jmax']),
            'SPECTRUM': set(['mass1', 'mass2', 'rmin', 'rmax', 'jmax', 'v1', 'v2']),
            'FIT':      set(['mass1', 'mass2', 'rmin', 'rmax'])
        }

        if set(tmp.keys()) != params_check[rtype]:
            sys.exit(f'ERROR:  for {rtype} the only following parameters must be given: {params_check[rtype]}')

        self.update(tmp)
        self['rtype'] = rtype

    def print_pec_params(
            self
        ) -> None:
        '''
        print params from dict in custom format
        '''
        print(f"[{self['ptype']}]")
        print(f"de    {self['de']}")
        print(f"re    {self['re']}")
        print(f"rref  {self['rref']}")
        print(f"q     {self['q']}")

        print('beta  ', end = '')
        for beta in self['beta']:
            print(f'{beta}\n      ', end = '')
        print()

#=======================================================================
#=======================================================================

def print_input_file(
        fname: str
    ) -> None:
    '''
    print file line-by-line
    '''
    if os.path.isfile(fname):
        print(f'\n=== Input file: {fname} ===\n')
        with open(fname, encoding="utf-8") as inp:
            for line in inp:
                print(line, end = '')
        print(f'\n=== End of input file: {fname} ===\n')
    else:
        sys.exit(f'ERROR: No such file: {fname}')

#=======================================================================

def print_pecs(
        pec: PWcurve,
        params: Dict[str, Any]
    ) -> None:
    '''
    print point-wise and approximated pec
    '''
    hdr = f'U({params["ptype"]}),cm-1'
    print(f'{"R,A":>10}{"U(p-w),cm-1":>20}{hdr:>20}{"delta,cm-1":>20}')

    # loop over r
    for r_inp, u_inp in zip(pec.rval, pec.cval):
        if params['ptype'] == 'EMO':
            u_cal = emo(r_inp, params)
        else:
            sys.exit(f"ERROR: {params['ptype']} not implemented")
        print(f'{r_inp:10.5f}{u_inp:20.5f}{u_cal:20.5f}{u_inp - u_cal:20.5f}')

#=======================================================================

def emo(
        r_inp: float,
        params: Dict[str, Any]
    ) -> float:
    '''
    calculate EMO value for given r point and params
    '''

    # EMO calc
    y = (r_inp**params['q'] - params['rref']**params['q']) / \
        (r_inp**params['q'] + params['rref']**params['q'])

    beta_pol = 0.
    for n, beta in enumerate(params['beta']):
        beta_pol += beta * y**n

    return params['de'] * (1 - np.exp(- beta_pol * (r_inp - params['re'])))**2   # type: ignore

#=======================================================================

def res_pec(
        guess: List[float],
        pec: PWcurve,
        params: Parameters
    ) -> List[float]:
    '''
    residual for pec_fit
    '''
    # fitted params
    tmp = Parameters()
    tmp.update(params)
    tmp['de'] = guess[0]
    tmp['re'] = guess[1]
    tmp['beta'] = guess[2:]

    # residual calc
    res = []

    for r_inp, u_inp in zip(pec.rval, pec.cval):
        if params['ptype'] == 'EMO':
            u_cal = emo(r_inp, tmp)
        else:
            sys.exit(f"ERROR: {params['ptype']} not implemented")
        err = max(u_inp / 100., 100.)
        res.append((u_cal - u_inp) / err)

    return res

#=======================================================================

def pec_fit(
        pec: PWcurve,
        params: Parameters
    ) -> Tuple[Parameters, str, bool]:
    '''
    fit pec by EMO function
    '''

    # fitted params
    guess = [params['de'], params['re']]
    guess.extend(params['beta'])
    add_args = (pec, params)

    # scipy least squares
    res_1 = least_squares(res_pec, guess, args = add_args)

    # out
    tmp = Parameters() #| params
    tmp.update(params)
    tmp['de'] = res_1.x[0]
    tmp['re'] = res_1.x[1]
    tmp['beta'] = np.array(list(res_1.x[2:]))

    return tmp, res_1.message, res_1.success

#=======================================================================

def read_expdata(
        fname: str
    ) -> Dict[int, Dict[int, float]]:
    '''
    read exp vib-rot levels
    '''
    input_parser = ConfigParser(delimiters=(' ', '\t'))
    input_parser.read(fname)

    # read levels
    expdata = {}
    n_levels = 0

    for j in input_parser.sections():
        tmp = {}
        for v, en in input_parser[j].items():
            tmp[int(v)] = float(en)
            n_levels += 1
        expdata[int(j)] = tmp

    # check
    if n_levels == 0:
        sys.exit(f'No energy levels found in {fname}')

    return expdata

#=======================================================================

def res_exp(
        guess: List[float],
        params: Parameters,
        pec: PWcurve,
        expdata: Dict[int, Dict[int, float]]
    ) -> List[float]:
    '''
    residual for exp_fit
    '''

    # fitted params
    tmp = Parameters()
    tmp.update(params)

    tmp['de'] = guess[0]
    tmp['re'] = guess[1]
    tmp['beta'] = guess[2:]

    levels = Levels('an', tmp, pec)

    # residual calc
    res = []

    # exp levels
    for j, en_jv in expdata.items():
        for v, en_v in en_jv.items():
            if j in levels.energy:
                if v in levels.energy[j]:
                    res.append((levels.energy[j][v] - en_v) / 0.1)

    # pec
    for r_inp, u_inp in zip(pec.rval, pec.cval):
        u_cal = emo(r_inp, tmp)
        err = max(u_inp / 100., 100.)
        res.append((u_cal - u_inp) / err)

    return res

#=======================================================================

def exp_fit(
        params: Parameters,
        pec: PWcurve,
        expdata: Dict[int, Dict[int, float]]
    ) -> Tuple[Parameters, str, bool]:
    '''
    fit pec to exp vib-rot levels
    '''

    # fitted params
    guess = [params['de'], params['re']]
    guess.extend(params['beta'])
    add_args = (params, pec, expdata)

    # scipy least squares
    res_1 = least_squares(res_exp, guess, args = add_args)

    # out
    tmp = Parameters()
    tmp.update(params)
    tmp['de'] = res_1.x[0]
    tmp['re'] = res_1.x[1]
    tmp['beta'] = np.array(list(res_1.x[2:]))

    return tmp, res_1.message, res_1.success

#=======================================================================
