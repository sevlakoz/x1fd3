from x1fd3.base import PWCurve, \
                       Levels
from .driver import Driver

class DriverLevelsPW(Driver):
    '''
    Driver for LevelsPW mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'ENERGY')
        self.pec = PWCurve(self.input_files[1])

    def core(
        self
    ) -> None:
        # calc and print vr levels
        Levels('pw', self.params, self.pec).print(self.out)
