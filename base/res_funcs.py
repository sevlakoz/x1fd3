'''
residual functions for fit_* functions to provide to scipy.optimize.least_squares
'''
import sys
from typing import Dict, List

from base.classPWcurve import PWcurve
from base.classParameters import Parameters
from base.classLevels import Levels
from base.emo import emo

def res_pec(
        guess: List[float],
        pec: PWcurve,
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

    for r_inp, u_inp in zip(pec.rval, pec.cval):
        if params['ptype'] == 'EMO':
            u_cal = emo(r_inp, tmp)
        else:
            sys.exit(f"ERROR: {params['ptype']} not implemented")
        err = max(u_inp / 100., 100.)
        res.append((u_cal - u_inp) / err)

    return res


def res_exp(
        guess: List[float],
        params: Parameters,
        pec: PWcurve,
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
    for r_inp, u_inp in zip(pec.rval, pec.cval):
        u_cal = emo(r_inp, tmp)
        err = max(u_inp / 100., 100.)
        res.append((u_cal - u_inp) / err)

    return res
