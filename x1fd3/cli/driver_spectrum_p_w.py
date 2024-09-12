from x1fd3.base.p_w_curve import PWCurve
from x1fd3.base.levels import Levels
from x1fd3.base.matrix_elements import MatrixElements
from .driver import Driver

class DriverSpectrumPW(Driver):
    '''
    Driver for SpectrumPW mode
    '''
    def read_files(
        self
    ) -> None:
        self.params.read_vr_calc_params(self.input_files[0], 'SPECTRUM')
        self.pec = PWCurve(self.input_files[1])
        self.dm = PWCurve(self.input_files[2])

    def core(
        self
    ) -> None:
        # calc vr levels
        levels = Levels('pw', self.params, self.pec)
        # calc and print integrals
        matrix_elements = MatrixElements(self.params, levels, self.dm)
        matrix_elements.print(self.out)
