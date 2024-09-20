'''
function for print not included in any class
'''
from os.path import isfile
from .p_w_curve import PWCurve
from .parameters import Parameters
from .logger import Logger
from .an_pec import AnPec

def print_input_file(
        out: Logger,
        fname: str
    ) -> None:
    '''
    print file line-by-line
    '''
    if isfile(fname):
        out.print(f'\n=== Input file: {fname} ===\n')
        with open(fname, encoding="utf-8") as inp:
            for line in inp:
                out.print(line, end = '')
        out.print(f'\n=== End of input file: {fname} ===\n')
    else:
        raise FileNotFoundError(f'No such file: {fname}')

def print_pecs(
        out: Logger,
        pec: PWCurve,
        params: Parameters
    ) -> None:
    '''
    print point-wise and approximated pec
    '''
    # pec calc
    pec_an = AnPec(params).calc(pec.rval)

    # print with loop over r
    lbl = f'U({params["ptype"]}),cm-1'
    out.print(f'{"R,A":>10}{"U(p-w),cm-1":>20}{lbl:>20}{"delta,cm-1":>20}')
    for r_inp, u_inp, u_cal in zip(pec.rval, pec.cval, pec_an):
        out.print(f'{r_inp:10.5f}{u_inp:20.3f}{u_cal:20.3f}{u_inp - u_cal:20.3f}')
