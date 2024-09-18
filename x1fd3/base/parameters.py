from configparser import ConfigParser
from collections import UserDict
import numpy as np

from .logger import Logger

class Parameters(UserDict):
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
            raise RuntimeError(f'Two or more analytic functions given in "{fname}"')

        ptype = input_parser.sections()[0]

        params_check = {
            'EMO': {'re', 'de', 'rref', 'q', 'beta'},
            'MLR': {'re', 'de', 'rref', 'q', 'p', 'beta', 'cnpow', 'cnval'},
            'DELR': {'re', 'de', 'rref', 'q', 'beta', 'cnpow', 'cnval'}
        }

        if not ptype in params_check.keys():
            raise RuntimeError(f'Uknown potential type "{ptype}"')

        tmp = {}

        for keyword, value in input_parser[ptype].items():
            if keyword in ('q', 'p'):
                tmp[keyword] = int(value)
            elif keyword in ('re', 'de', 'rref'):
                tmp[keyword] = float(value)                              # type: ignore
            elif keyword in ('beta', 'cnval'):
                tmp[keyword] = np.array(list(map(float, value.split()))) # type: ignore
            elif keyword in ('cnpow'):
                tmp[keyword] = np.array(list(map(int, value.split()))) # type: ignore

        if tmp.keys() != params_check[ptype]:
            raise RuntimeError(f'For {ptype} the following parameters must be given: {params_check[ptype]}')

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
            raise RuntimeError(f'Uknown run type "{rtype}"')

        # read calc params
        input_parser = ConfigParser(delimiters=(' ', '\t'))
        input_parser.read(fname)

        if len(input_parser.sections()) > 1:
            raise RuntimeError(f'Two or more sets of parameters given in "{fname}"')

        if input_parser.sections()[0] != rtype:
            raise RuntimeError(f'run type in "{fname}" is not consistent with the actual run type')

        tmp = {}

        for keyword, value in input_parser[rtype].items():
            if keyword in ('jmax', 'v1', 'v2'):
                tmp[keyword] = int(value)
            elif keyword in ('mass1', 'mass2', 'rmin', 'rmax'):
                tmp[keyword] = float(value)                        # type: ignore

        params_check = {
            'ENERGY':   {'mass1', 'mass2', 'rmin', 'rmax', 'jmax'},
            'SPECTRUM': {'mass1', 'mass2', 'rmin', 'rmax', 'jmax', 'v1', 'v2'},
            'FIT':      {'mass1', 'mass2', 'rmin', 'rmax'}
        }

        if tmp.keys() != params_check[rtype]:
            raise RuntimeError(f'for {rtype} the only following parameters must be given: {params_check[rtype]}')

        self.update(tmp)
        self['rtype'] = rtype

    def print_pec_params(
            self,
            out: Logger
        ) -> None:
        '''
        print params from dict in custom format
        '''
        out.print(f"[{self['ptype']}]")
        out.print(f"de    {self['de']:.3f}")
        out.print(f"re    {self['re']:.6f}")
        out.print(f"rref  {self['rref']:.6f}")
        out.print(f"q     {self['q']}")

        if self['ptype'] == 'MLR':
            out.print(f"p     {self['p']}")

        lbl = 'beta  '
        for beta in self['beta']:
            out.print(f'{lbl}{beta:10.5e}')
            lbl = ' '*6

        if self['ptype'] in ('MLR', 'DELR'):
            lbl = 'cnpow '
            for n in self['cnpow']:
                out.print(f'{lbl}{n:<2d}')
                lbl = ' '*6
            lbl = 'cnval '
            for cn in self['cnval']:
                out.print(f'{lbl}{cn:10.5e}')
                lbl = ' '*6
