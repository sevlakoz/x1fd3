import numpy as np
from scipy.optimize import least_squares      # type: ignore

from .p_w_curve import PWCurve
from .parameters import Parameters
from .exp_data import ExpData
from .levels import Levels
from .an_pec import AnPec
from .logger import Logger

class Fit:
    '''
    least square fit 
    a) pec approximation if no exp. levels provided
    b) fit pec to exp. levels otherwise
    '''
    def __init__(
        self,
        params:Parameters,
        pec:PWCurve,
        expdata:ExpData
    ) -> None:
        '''
        set input data
        '''
        self.params = params
        self.pec = pec
        self.expdata = expdata
        self.mes = 'not fitted'


    def fit(
        self
    ) -> str:
        '''
        perform least square fit
        '''
        # params -> guess
        guess = [self.params['de'], self.params['re']]
        guess.extend(self.params['beta'])

        # scipy least squares
        res_1 = least_squares(self._res, guess)
        if res_1.success:
            self.mes = f'PEC fit done: {res_1.message}'
        else:
            raise RuntimeError(f'\nfit FAILED: {res_1.message}')

        # fit result -> params
        self.params['de'] = res_1.x[0]
        self.params['re'] = res_1.x[1]
        self.params['beta'] = np.array(list(res_1.x[2:]))

        return self.mes


    def print_state(
        self,
        label:str,
        out:Logger
    ) -> None:
        '''
        print pec and exp levels if provided at init
        '''
        if self.expdata.nlev > 0:
            out.print(f'{label} levels')
            Levels(self.params, PWCurve(), self.expdata).print_with_expdata(out)
        out.print(f'{label} PEC\n')
        self.pec.print_with_anpec(self.params, out)
        out.print(f'\n{label} parameters\n')
        self.params.print_pec_params(out)


    def _res(
        self,
        guess:list[float]
    ) -> list[float]:
        '''
        residual for fit
        '''
        # fitted params
        tmp = Parameters()
        tmp.update(self.params)

        tmp['de'] = guess[0]
        tmp['re'] = guess[1]
        tmp['beta'] = guess[2:]

        # residual calc
        res:list[float] = []

        # exp levels
        if self.expdata.nlev > 0:
            levels = Levels(tmp, PWCurve(), self.expdata)
            for j, en_jv in self.expdata.energy.items():
                for v, en_v in en_jv.items():
                    res.append((levels.energy[j][v] - en_v) / 0.1)

        # pec
        pec_an = AnPec(tmp).calc(self.pec.rvs)
        res.extend((self.pec.cvs - pec_an) / self.pec.evs)

        return res
