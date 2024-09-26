from x1fd3.base import Levels, \
                       PWCurve, \
                       ExpData
from .driver import Driver

class DriverLevelsAn(Driver):
    '''
    Driver for LevelsAn mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'ENERGY')
        self.params.read_pec_params(self.input_files[1])

    def core(
        self
    ) -> None:
        # calc and print vr levels
        Levels(self.params, PWCurve(), ExpData()).print(self.out)
