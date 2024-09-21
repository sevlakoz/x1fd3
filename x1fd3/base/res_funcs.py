'''
residual functions for fit_* functions to provide to scipy.optimize.least_squares
'''
from .p_w_curve import PWCurve
from .parameters import Parameters
from .levels import Levels
from .exp_data import ExpData
from .an_pec import AnPec

def res_pec(
        guess: list[float],
        pec: PWCurve,
        params: Parameters
    ) -> list[float]:
    '''
    residual for pec_fit
    '''
    # fitted params
    tmp = Parameters()
    tmp.update(params)
    tmp['de'] = guess[0]
    tmp['re'] = guess[1]
    tmp['beta'] = guess[2:]

    # pec
    pec_an = AnPec(tmp).calc(pec.rval)

    # residual calc
    res = list((pec.cval - pec_an) / pec.eval)

    return res


def res_exp(
        guess: list[float],
        params: Parameters,
        pec: PWCurve,
        expdata: ExpData
    ) -> list[float]:
    '''
    residual for exp_fit
    '''

    # fitted params
    tmp = Parameters()
    tmp.update(params)

    tmp['de'] = guess[0]
    tmp['re'] = guess[1]
    tmp['beta'] = guess[2:]

    levels = Levels('an', tmp, pec)

    # residual calc
    res = []

    # exp levels
    for j, en_jv in expdata.energy.items():
        for v, en_v in en_jv.items():
            if j in levels.energy and v in levels.energy[j]:
                res.append((levels.energy[j][v] - en_v) / 0.1)

    # pec
    pec_an = AnPec(tmp).calc(pec.rval)
    res.extend((pec.cval - pec_an) / pec.eval)

    return res
