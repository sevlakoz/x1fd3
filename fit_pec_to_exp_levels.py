import sys

from funcs import *

if len(sys.argv) < 5:
	exit('Usage: python fit_pec_to_exp_levels.py <file with parameters for level calc|example: vr_fit_params.txt> <file with pre-fitted parameters|example: emo_params.txt> <file with point-wise pec|example: pec.txt> <file with exp. vr levels|example: levels.txt>')

f_vr_par = sys.argv[1]
f_fit_par = sys.argv[2]
f_pw_pec = sys.argv[3]
f_epx_lev = sys.argv[4]

# print input
print_input_file(f_vr_par)
print_input_file(f_fit_par)
print_input_file(f_pw_pec)
print_input_file(f_epx_lev)

# read files
rp, up = read_pw_curve(f_pw_pec)
params = read_pec_pars(f_fit_par)
params = params | read_vr_calc_pars(f_vr_par, 'FIT')
expdata = read_expdata(f_epx_lev)

params['jmax'] = max(expdata.keys())

print('=== Fit PEC to reproduce exp. data ===\n')

# print initial guess
print('Initial guess')
levels = vr_solver('an', params)
print_levels_n_expdata(params, levels, expdata)
print_pecs(rp, up, params)

# fit
params, message, success = exp_fit(params, rp, up, expdata)
if success:
	print(f'\nPEC fit done: {message}')
else:
	exit(f'\nPEC fit FAILED: {message}')

# print final results
print('Fit results')
levels = vr_solver('an', params)
print_levels_n_expdata(params, levels, expdata)
print_pecs(rp, up, params)
print('\nFitted parameters\n')
print_params(params)
