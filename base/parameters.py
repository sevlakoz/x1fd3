from configparser import ConfigParser
from collections import UserDict
import numpy as np


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
            raise RuntimeError(f'ERROR: Two or more analytic functions given in "{fname}"')

        ptype = input_parser.sections()[0]

        if not ptype in ['EMO']:
            raise RuntimeError(f'ERROR:  Uknown potential type "{ptype}"')

        tmp = {}

        for keyword, value in input_parser[ptype].items():
            if keyword in ('q'):
                tmp[keyword] = int(value)
            elif keyword in ('re', 'de', 'rref'):
                tmp[keyword] = float(value)                              # type: ignore
            elif keyword in ('beta'):
                tmp[keyword] = np.array(list(map(float, value.split()))) # type: ignore

        params_check = {
            'EMO': {'re', 'de', 'rref', 'q', 'beta'}
        }

        if tmp.keys() != params_check[ptype]:
            raise RuntimeError(f'ERROR:  for {ptype} the following parameters must be given: {params_check[ptype]}')

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
            raise RuntimeError(f'ERROR:  Uknown run type "{rtype}"')

        # read calc params
        input_parser = ConfigParser(delimiters=(' ', '\t'))
        input_parser.read(fname)

        if len(input_parser.sections()) > 1:
            raise RuntimeError(f'ERROR: Two or more sets of parameters given in "{fname}"')

        if input_parser.sections()[0] != rtype:
            raise RuntimeError(f'ERROR: run type in "{fname}" is not consistent with the actual run type')

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
            raise RuntimeError(f'ERROR:  for {rtype} the only following parameters must be given: {params_check[rtype]}')

        self.update(tmp)
        self['rtype'] = rtype

    def print_pec_params(
            self
        ) -> None:
        '''
        print params from dict in custom format
        '''
        print(f"[{self['ptype']}]")
        print(f"de    {self['de']:.3f}")
        print(f"re    {self['re']:.6f}")
        print(f"rref  {self['rref']:.6f}")
        print(f"q     {self['q']}")

        print('beta  ', end = '')
        for beta in self['beta']:
            print(f'{beta:10.5e}\n      ', end = '')
        print()
