import sys

from funcs import *

if len(sys.argv) < 5:
	exit('Usage: python fit_pec_to_exp_levels.py <file with parameters for level calc|example: vr_level_calc_params.txt> <file with pre-fitted parameters|example: emo_params.txt> <file with point-wise pec|example: pec.txt> <file with exp. vr levels|example: levels.txt>')

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
params = params | read_vr_calc_pars(f_vr_par, 'ENERGY')
expdata = read_expdata(f_epx_lev)

if params['jmax'] < max(expdata.keys()):
	print(f'only exp. levels with J = {params["jmax"]} are included to the fit procedure')
else:
	params['jmax'] = max(expdata.keys())

print('=== Fit PEC to reproduce exp. data ===\n')

# print initial guess
print('Initial guess')
levels = vr_solver('an', params)
print(f'\n   J   v      Eexp,cm-1     Ecalc,cm-1     delta,cm-1')
for j in expdata.keys():
	if j > params['jmax']:
		continue
	for v in expdata[j].keys():
		ee = expdata[j][v]
		ec = levels[j][v].energy
		print(f'{j:4d}{v:4d}{ee:15.8f}{ec:15.5f}{ee - ec:15.5f}')
print()
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
print(f'\n   J   v      Eexp,cm-1     Ecalc,cm-1     delta,cm-1')
for j in expdata.keys():
	if j > params['jmax']:
		continue
	for v in expdata[j].keys():
		ee = expdata[j][v]
		ec = levels[j][v].energy
		print(f'{j:4d}{v:4d}{ee:15.8f}{ec:15.5f}{ee - ec:15.5f}')
print()
print_pecs(rp, up, params)
print('\nFitted parameters\n')
print_params(params)
