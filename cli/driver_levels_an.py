from base.levels import Levels
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
        levels = Levels('an', self.params)
        levels.print()
