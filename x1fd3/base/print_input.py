'''
function for print not included in any class
'''
from os.path import isfile
from .logger import Logger

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


