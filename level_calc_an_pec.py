import sys

from funcs import print_input_file, Parameters, Levels

if len(sys.argv) < 3:
    sys.exit(
    '''Usage: python level_cacl_an_pec.py <1> <2>
    <1> = file with parameters for level calc | example: vr_level_calc_params.txt
    <2> = file with fitted parameters         | example: fitted_emo_params.txt'''
    )

f_vr_par = sys.argv[1]
f_fit_par = sys.argv[2]

# print input
print_input_file(f_vr_par)
print_input_file(f_fit_par)

# read files
params = Parameters()
params.read_pec_params(f_fit_par)
params.read_vr_calc_params(f_vr_par, 'ENERGY')

# calc and print vr levels
levels = Levels('an', params)
levels.print()
