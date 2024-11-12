from abc import ABC, abstractmethod
from os.path import isfile

from x1fd3.base import PWCurve, \
                       Parameters, \
                       Logger, \
                       ExpData

class Driver(ABC):
    '''
    abstract class for driver, 
    contains input, data for input check, empty vars, & Logger for output
    '''
    def __init__(
        self,
        input_files:list[str],
        out:Logger
    ):
        '''
        set empty vars
        check number of input files provided
        print error message if not enough for chosen run mode
        '''
        self.mode:str = type(self).__name__.replace('Driver', '')
        self.input_files:list[str] = input_files

        input_error_message:dict[str, tuple[int, str]] = {
            'PecApprox': (
                2,
                'Usage: python -m x1fd3 PecApprox <1> <2>\n' + 
                '       <2> = file with initial parameters | example: input/init_emo.txt\n' +
                '       <1> = file with point-wise pec     | example: input/pw_pec.txt'
            ),
            'LevelsPW': (
                2,
                'Usage: python -m x1fd3 LevelsPW <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: input/params_levels.txt\n' +
                '       <2> = file with point-wise pec            | example: input/pw_pec.txt'
            ),
            'LevelsAn': (
                2,
                'Usage: python -m x1fd3 LevelsAn <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: input/params_levels.txt\n' +
                '       <2> = file with fitted parameters         | example: input/fitted_emo.txt'
            ),
            'SpectrumPW': (
                3,
                'Usage: python -m x1fd3 SpectrumPW <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: input/params_spectrum.txt\n' +
                '       <2> = file with point-wise pec               | example: input/pw_pec.txt\n' +
                '       <3> = file with point-wise dm                | example: input/pw_dm.txt'
            ),
            'SpectrumAn': (
                3,
                'Usage: python -m x1fd3 SpectrumAn <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: input/params_spectrum.txt\n' +
                '       <2> = file with fitted parameters            | example: input/fitted_emo.txt\n' +
                '       <3> = file with point-wise dm                | example: input/pw_dm.txt'
            ),
            'FitExp': (
                4,
                'Usage: python -m x1fd3 FitExp <1> <2> <3> <4>\n' +
                '       <1> = file with parameters for level calc | example: input/params_fit.txt\n' +
                '       <2> = file with pre-fitted parameters     | example: input/fitted_emo.txt\n' +
                '       <3> = file with point-wise pec            | example: input/pw_pec.txt\n' +
                '       <4> = file with exp. vib.-rot. levels     | example: input/exp_levels.txt'
            )
        }

        nf, mes = input_error_message[self.mode]
        if len(input_files) < nf:
            raise RuntimeError('Missing command line arguments: input files\n' + mes)

        self.pec = PWCurve()
        self.dm = PWCurve()
        self.params = Parameters()
        self.expdata = ExpData()
        self.out = out

    def print_input_files(
        self
    ) -> None:
        '''
        print input files one by one
        '''
        input_file_types:dict[str, tuple[str, ...]] = {
            'PecApprox': (
                'Init PEC parameters',
                'Point-wise PEC'
            ),
            'LevelsPW': (
                'Parameter for levels calculation',
                'Point-wise PEC'
            ),
            'LevelsAn': (
                'Parameter for levels calculation',
                'Fitted PEC parameters'
            ),
            'SpectrumPW': (
                'Parameter for spectrum calculation',
                'Point-wise PEC',
                'Point-wise dipole moment'
            ),
            'SpectrumAn': (
                'Parameter for spectrum calculation',
                'Fitted PEC parameters',
                'Point-wise dipole moment'
            ),
            'FitExp': (
                'Parameters for fit',
                'Fitted PEC parameters',
                'Point-wise PEC',
                'Experimental levels'
            )
        }

        self.out.print('Input files:', *self.input_files)
        for fname, ftype in zip(self.input_files, input_file_types[self.mode]):
            if isfile(fname):
                self.out.print(f'* {ftype} *')
                self.out.print(f'\n=== Input file: {fname} ===\n')
                with open(fname, encoding='utf-8') as inp:
                    for line in inp:
                        self.out.print(line, end='')
                self.out.print(f'\n=== End of input file: {fname} ===\n')
            else:
                raise FileNotFoundError(f'No such file: {fname}')

    @abstractmethod
    def read_files(
        self
    ) -> None:
        '''
        read files, store to vars
        '''

    @abstractmethod
    def core(
        self
    ) -> None:
        '''
        run calc & print stuff
        '''

    def run(
        self
    ) -> None:
        '''
        run all task
        '''
        self.print_input_files()
        self.read_files()
        self.core()
