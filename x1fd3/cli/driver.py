import traceback
from abc import ABC, abstractmethod
from time import time

from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.parameters import Parameters
from x1fd3.base.logger import Logger
from x1fd3.base.exp_data import ExpData
from x1fd3.base.print_funcs import print_input_file

class Driver(ABC):
    '''
    abstract class for driver, 
    contains input, data for input check, empty vars, & Logger for output
    '''
    def __init__(
        self,
        input_files: list[str]
    ):
        '''
        set empty vars, create Logger
        check number of input files provided
        print error message if not enough for chosen run mode
        '''
        self.mode:str = type(self).__name__.replace('Driver', '')
        self.input_files: list[str] = input_files

        input_error_message: dict[str, tuple[int, str]] = {
            'PecApprox': (
                2,
                'Usage: python -m x1fd3 PecApprox <1> <2>\n' + 
                '       <1> = file with point-wise pec     | example: input/pw_pec.txt\n' +
                '       <2> = file with initial parameters | example: input/init_emo.txt'
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
        self.out = Logger(self.mode)

    def print_input_files(
        self
    ) -> None:
        '''
        print input files one by one
        '''
        self.out.print('Input files:', *self.input_files)
        for fname in self.input_files:
            print_input_file(self.out, fname)

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
        run all task, print info
        '''
        start = time()
        try:
            self.print_input_files()
            self.read_files()
            self.core()
            print('Success!')
        except BaseException: # pylint: disable = W0718
            print('Error!')
            err = traceback.format_exc()
            self.out.print(err)
            print(err)
        finish = time()
        print(f'Execution time, s: {finish - start:.3f}')
        print(f'Results stored in {self.out.fname}')
