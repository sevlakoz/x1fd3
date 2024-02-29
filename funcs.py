import os
import numpy as np
from configparser import ConfigParser
from scipy.optimize import least_squares

#=======================================================================

def print_input_file(fname):
	if os.path.isfile(fname):
		print(f'\n=== Input file: {fname} ===\n')
		with open(fname) as inp:
			for line in inp:
				print(line, end = '')
		print(f'\n=== End of input file: {fname} ===\n')
	else:
		exit(f'ERROR: No such file: {fname}')

#=======================================================================

def read_pw_curve(fname):
	
	r = []
	c = []
	
	with open(fname) as inp:
		for line in inp:
			if line.lstrip() == '' or line.lstrip()[0] == '#':
				continue
			line = line.split()
			r.append(float(line[0]))
			c.append(float(line[1]))
	
	r = np.array(r)
	c = np.array(c)
	
	return r, c

#=======================================================================

def read_pec_pars(fname):
	
	input_parser = ConfigParser(delimiters=(' ', '\t'))
	input_parser.read(fname)
	
	params = {}
	
	if len(input_parser.sections()) > 1:
		exit(f'ERROR: Two or more analytic functions given in "{fname}"')
	
	pot = input_parser.sections()[0]
	
	if not pot in ['EMO']:
		exit(f'ERROR:  Uknown potential type "{pot}"')
	
	for keyword, value in input_parser[pot].items():
		if keyword in ('q'):
			params[keyword] = int(value)
		elif keyword in ('re', 'de', 'rref'):
			params[keyword] = float(value)
		elif keyword in ('beta'):
			params[keyword] = np.array(list(map(float, value.split())))
	
	params_check = {
		'EMO': set(['re', 'de', 'rref', 'q', 'beta'])
	}
	
	if set(params.keys()) != params_check[pot]:
		exit(f'ERROR:  for {pot} the following parameters must be given: {params_check[pot]}')
	
	params['type'] = pot
	
	return params

#=======================================================================

def emo(r, de, re, rref, q, beta):
	
	y = (r**q - rref**q) / (r**q + rref**q)
	
	beta_pol = beta[0]
	for n in range(1, len(beta)):
		beta_pol += beta[n] * y**n
		
	return de * (1 - np.exp(-beta_pol * (r - re)))**2

#=======================================================================

def print_pecs(rp, up, params):
	
	print(f'                 R,A         U(p-w),cm-1         U({params["type"]}),cm-1')
	for r, u in zip(rp, up):
		if params['type'] == 'EMO':
			ua = emo(r, params['de'], params['re'], params['rref'], params['q'], params['beta'])
		print(f'{r:20.5f}{u:20.5f}{ua:20.5f}')

#=======================================================================

def print_params(params):
	print(f"[{params['type']}]")
	print(f"de    {params['de']}")
	print(f"re    {params['re']}")
	print(f"rref  {params['rref']}")
	print(f"q     {params['q']}")
	print('beta  ', end = '')
	for b in params['beta']:
		print(f'{b}\n      ', end = '')


#=======================================================================

def res_pec_fit(guess, rp, up, params): 
	
	de = guess[0]
	re = guess[1]
	beta = guess[2:]
	
	res = []
	for r, u in zip(rp, up):
		if params['type'] == 'EMO':
			ua = emo(r, de, re, params['rref'], params['q'], beta)
		res.append((ua - u) / 100.)
	
	return res

#=======================================================================

def pec_fit(rp, up, params):
	
	guess = [params['de'], params['re']]
	guess.extend(params['beta'])
	add_args = (rp, up, params)
	res_1 = least_squares(res_pec_fit, guess, args = add_args)
	
	params['de'] = res_1.x[0]
	params['re'] = res_1.x[1]
	params['beta'] = np.array(list(res_1.x[2:]))
	
	return params, res_1.message, res_1.success

#=======================================================================
