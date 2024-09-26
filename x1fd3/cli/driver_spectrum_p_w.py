from x1fd3.base import PWCurve, \
                       Levels, \
                       ExpData, \
                       MatrixElements
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
        levels = Levels(self.params, self.pec, ExpData())
        # calc and print integrals
        MatrixElements(self.params, levels, self.dm).print(self.out)
