import sys

from base.print_funcs import print_input_file
from base.classPWcurve import PWcurve
from base.classParameters import Parameters
from base.classLevels import Levels
from base.classMatrixElements import MatrixElements

if len(sys.argv) < 4:
    sys.exit(
    '''Usage: python spectrum_cacl_an_pec.py <1> <2> <3>
    <1> = file with parameters for spectrum calc | example: vr_spectrum_calc_params.txt
    <2> = file with fitted parameters            | example: fitted_emo_params.txt
    <3> = file with point-wise dm                | example: pw_dm.txt'''
    )

f_vr_par = sys.argv[1]
f_fit_par = sys.argv[2]
f_pw_dm = sys.argv[3]

# print input
print_input_file(f_vr_par)
print_input_file(f_fit_par)
print_input_file(f_pw_dm)

# read files
params = Parameters()
params.read_pec_params(f_fit_par)
params.read_vr_calc_params(f_vr_par, 'SPECTRUM')
dm = PWcurve(f_pw_dm)

# calc vr levels
levels = Levels('an', params)

# calc and print integrals
matrix_elements = MatrixElements(params, levels, dm)
matrix_elements.print()
