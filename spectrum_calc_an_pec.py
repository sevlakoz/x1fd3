import sys

from funcs import *

if len(sys.argv) < 4:
	exit('''Usage: python spectrum_cacl_an_pec.py <1> <2> <3>
       <1> = file with parameters for spectrum calc | example: vr_spectrum_calc_params.txt
       <2> = file with fitted parameters            | example: emo_params.txt
       <3> = file with point-wise dm                | example: dm.txt''')

f_vr_par = sys.argv[1]
f_fit_par = sys.argv[2]
f_pw_dm = sys.argv[3]

# print input
print_input_file(f_vr_par)
print_input_file(f_fit_par)
print_input_file(f_pw_dm)

# read files
params = read_pec_pars(f_fit_par)
params = params | read_vr_calc_pars(f_vr_par, 'SPECTRUM')
rd, fd = read_pw_curve(f_pw_dm)

# calc and print vr levels
levels = vr_solver('an', params)
print_levels(levels)

# calc and print integrals
matrix_elements = me_calc(params, levels, rd, fd)
print_matrix_elements(params, levels, matrix_elements)
