from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.levels import Levels
from x1fd3.base.matrix_elements import MatrixElements
from .driver import Driver

class DriverSpectrumAn(Driver):
    '''
    Driver for SpectrumAn mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'SPECTRUM')
        self.params.read_pec_params(self.input_files[1])
        self.dm = PWCurve(self.input_files[2])

    def core(
        self
    ) -> None:
        # calc vr levels
        levels = Levels('an', self.params)
        # calc and print integrals
        MatrixElements(self.params, levels, self.dm).print(self.out)
