'''
residual functions for fit_* functions to provide to scipy.optimize.least_squares
'''
from typing import Dict, List

from .p_w_curve import PWCurve
from .parameters import Parameters
from .levels import Levels
from .emo import emo

def res_pec(
        guess: List[float],
        pec: PWCurve,
        params: Parameters
    ) -> List[float]:
    '''
    residual for pec_fit
    '''
    # fitted params
    tmp = Parameters()
    tmp.update(params)
    tmp['de'] = guess[0]
    tmp['re'] = guess[1]
    tmp['beta'] = guess[2:]

    # residual calc
    res = []

    # pec
    if params['ptype'] == 'EMO':
        pec_an = emo(pec.rval, tmp)
    else:
        raise RuntimeError(f"ERROR: {params['ptype']} not implemented")

    for u_inp, u_cal in zip(pec.cval, pec_an):
        err = max(u_inp / 100., 100.)
        res.append((u_cal - u_inp) / err)

    return res


def res_exp(
        guess: List[float],
        params: Parameters,
        pec: PWCurve,
        expdata: Dict[int, Dict[int, float]]
    ) -> List[float]:
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
    for j, en_jv in expdata.items():
        for v, en_v in en_jv.items():
            if j in levels.energy:
                if v in levels.energy[j]:
                    res.append((levels.energy[j][v] - en_v) / 0.1)

    # pec
    if params['ptype'] == 'EMO':
        pec_an = emo(pec.rval, tmp)
    else:
        raise RuntimeError(f"ERROR: {params['ptype']} not implemented")

    for u_inp, u_cal in zip(pec.cval, pec_an):
        err = max(u_inp / 100., 100.)
        res.append((u_cal - u_inp) / err)

    return res
