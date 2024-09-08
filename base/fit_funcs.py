'''
least square fit functions 
'''

from typing import Dict, Tuple
import numpy as np
from scipy.optimize import least_squares      # type: ignore

from base.classPWcurve import PWcurve
from base.classParameters import Parameters
from base.res_funcs import res_pec, res_exp

def pec_fit(
        pec: PWcurve,
        params: Parameters
    ) -> Tuple[Parameters, str, bool]:
    '''
    fit pec by EMO function
    '''

    # fitted params
    guess = [params['de'], params['re']]
    guess.extend(params['beta'])
    add_args = (pec, params)

    # scipy least squares
    res_1 = least_squares(res_pec, guess, args = add_args)

    # out
    tmp = Parameters() #| params
    tmp.update(params)
    tmp['de'] = res_1.x[0]
    tmp['re'] = res_1.x[1]
    tmp['beta'] = np.array(list(res_1.x[2:]))

    return tmp, res_1.message, res_1.success

def exp_fit(
        params: Parameters,
        pec: PWcurve,
        expdata: Dict[int, Dict[int, float]]
    ) -> Tuple[Parameters, str, bool]:
    '''
    fit pec to exp vib-rot levels
    '''

    # fitted params
    guess = [params['de'], params['re']]
    guess.extend(params['beta'])
    add_args = (params, pec, expdata)

    # scipy least squares
    res_1 = least_squares(res_exp, guess, args = add_args)

    # out
    tmp = Parameters()
    tmp.update(params)
    tmp['de'] = res_1.x[0]
    tmp['re'] = res_1.x[1]
    tmp['beta'] = np.array(list(res_1.x[2:]))

    return tmp, res_1.message, res_1.success
