'''
function for print not included in any class
'''
from os.path import isfile
from .p_w_curve import PWCurve
from .parameters import Parameters
from .emo import emo

def print_input_file(
        fname: str
    ) -> None:
    '''
    print file line-by-line
    '''
    if isfile(fname):
        print(f'\n=== Input file: {fname} ===\n')
        with open(fname, encoding="utf-8") as inp:
            for line in inp:
                print(line, end = '')
        print(f'\n=== End of input file: {fname} ===\n')
    else:
        raise FileNotFoundError(f'ERROR: No such file: {fname}')

def print_pecs(
        pec: PWCurve,
        params: Parameters
    ) -> None:
    '''
    print point-wise and approximated pec
    '''
    hdr = f'U({params["ptype"]}),cm-1'
    print(f'{"R,A":>10}{"U(p-w),cm-1":>20}{hdr:>20}{"delta,cm-1":>20}')

    # loop over r
    for r_inp, u_inp in zip(pec.rval, pec.cval):
        if params['ptype'] == 'EMO':
            u_cal = emo(r_inp, params)
        else:
            raise RuntimeError(f"ERROR: {params['ptype']} not implemented")
        print(f'{r_inp:10.5f}{u_inp:20.5f}{u_cal:20.5f}{u_inp - u_cal:20.5f}')
