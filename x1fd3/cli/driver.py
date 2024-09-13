from abc import ABC, abstractmethod
from time import time

from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.parameters import Parameters
from x1fd3.base.logger import Logger
from x1fd3.base.print_funcs import print_input_file

class Driver(ABC):
    '''
    base abs class for driver, 
    contains data for input check and empty vars
    '''
    def __init__(
        self,
        input_files: list[str]
    ):
        self.input_files: list[str] = input_files
        self.mode:str = type(self).__name__.replace('Driver', '')
        self.input_error_message: dict[str, tuple[int, str]] = {
            'PecApprox': (
                2,
                'Usage: python -m x1fd3 PecApprox <1> <2>\n' + 
                '       <1> = file with point-wise pec     | example: input/pw_pec.txt\n' +
                '       <2> = file with initial parameters | example: input/init_emo_params.txt'
            ),
            'LevelsPW': (
                2,
                'Usage: python -m x1fd3 LevelsPW <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: input/vr_level_calc_params.txt\n' +
                '       <2> = file with point-wise pec            | example: input/pw_pec.txt'
            ),
            'LevelsAn': (
                2,
                'Usage: python -m x1fd3 LevelsAn <1> <2>\n' +
                '       <1> = file with parameters for level calc | example: input/vr_level_calc_params.txt\n' +
                '       <2> = file with fitted parameters         | example: input/fitted_emo_params.txt'
            ),
            'SpectrumPW': (
                3,
                'Usage: python -m x1fd3 SpectrumPW <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: input/vr_spectrum_calc_params.txt\n' +
                '       <2> = file with point-wise pec               | example: input/pw_pec.txt\n' +
                '       <3> = file with point-wise dm                | example: input/pw_dm.txt'
            ),
            'SpectrumAn': (
                3,
                'Usage: python -m x1fd3 SpectrumAn <1> <2> <3>\n' +
                '       <1> = file with parameters for spectrum calc | example: input/vr_spectrum_calc_params.txt\n' +
                '       <2> = file with fitted parameters            | example: input/fitted_emo_params.txt\n' +
                '       <3> = file with point-wise dm                | example: input/pw_dm.txt'
            ),
            'FitExp': (
                4,
                'Usage: python -m x1fd3 FitExp <1> <2> <3> <4>\n' +
                '       <1> = file with parameters for level calc | example: input/vr_fit_params.txt\n' +
                '       <2> = file with pre-fitted parameters     | example: input/fitted_emo_params.txt\n' +
                '       <3> = file with point-wise pec            | example: input/pw_pec.txt\n' +
                '       <4> = file with exp. vib.-rot. levels     | example: input/exp_levels.txt'
            )
        }

        self.pec = PWCurve()
        self.dm = PWCurve()
        self.params = Parameters()
        self.expdata: dict[int, dict[int, float]] = {}
        self.out = Logger(self.mode)

    def input_check(
        self
    ) -> None:
        '''
        check count of input files
        print error message if not enough 
        '''
        nf, mes = self.input_error_message[self.mode]
        if len(self.input_files) < nf:
            raise RuntimeError('Missing command line arguments: input files\n' + mes)

    def print_input_files(
        self
    ) -> None:
        '''
        print input files one by one
        '''
        for fname in self.input_files:
            print_input_file(self.out, fname)

    @abstractmethod
    def read_files(
        self
    ) -> None:
        '''
        read files, store to vars, no pattern at all
        '''

    @abstractmethod
    def core(
        self
    ) -> None:
        '''
        run calc & print stuff, no pattern at all
        '''

    def run(
        self
    ) -> None:
        '''
        run all task, print info
        '''
        start = time()
        self.input_check()
        self.print_input_files()
        self.read_files()
        self.core()
        finish = time()
        print(f'Calculation time, s: {int(finish - start)}')
        print(f'Results stored in {self.out.fname}')
