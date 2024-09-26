from x1fd3.base import PWCurve, \
                       Levels, \
                       ExpData, \
                       MatrixElements
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
        levels = Levels(self.params, PWCurve(), ExpData())
        # calc and print integrals
        MatrixElements(self.params, levels, self.dm).print(self.out)
