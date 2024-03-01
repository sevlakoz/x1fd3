import os
import numpy as np
from dataclasses import dataclass
from configparser import ConfigParser
from scipy.optimize import least_squares
from scipy.interpolate import splrep, splev
from scipy.linalg import eigh_tridiagonal

#=======================================================================

@dataclass
class Level:
	energy: float
	rot_const: float
	r_grid: np.ndarray
	wavef_grid: np.ndarray

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
	
	params['ptype'] = pot
	
	return params

#=======================================================================

def read_vr_calc_pars(fname, rtype):
	
	if not rtype in ['ENERGY', 'SPECTRUM']:
		exit(f'ERROR:  Uknown run type "{rtype}"')
	
	input_parser = ConfigParser(delimiters=(' ', '\t'))
	input_parser.read(fname)
	
	params = {}
	
	if len(input_parser.sections()) > 1:
		exit(f'ERROR: Two or more sets of parameters given in "{fname}"')
	
	if input_parser.sections()[0] != rtype:
		exit(f'ERROR: run type in "{fname}" is not consistent with actual run type')
	
	for keyword, value in input_parser[rtype].items():
		if keyword in ('jmax', 'v1', 'v2'):
			params[keyword] = int(value)
		elif keyword in ('mass1', 'mass2', 'rmin', 'rmax'):
			params[keyword] = float(value)
	
	params_check = {
		'ENERGY': set(['mass1', 'mass2', 'rmin', 'rmax', 'jmax']),
		'SPECTRUM': set(['mass1', 'mass2', 'rmin', 'rmax', 'jmax', 'v1', 'v2'])
	}
	
	if set(params.keys()) != params_check[rtype]:
		exit(f'ERROR:  for {rtype} the only following parameters must be given: {params_check[rtype]}')
	
	params['rtype'] = rtype
	
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
	
	print(f'                 R,A         U(p-w),cm-1         U({params["type"]}),cm-1          delta,cm-1')
	for r, u in zip(rp, up):
		if params['ptype'] == 'EMO':
			ua = emo(r, params['de'], params['re'], params['rref'], params['q'], params['beta'])
		print(f'{r:20.5f}{u:20.5f}{ua:20.5f}{u - ua:20.5f}')

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
		if params['ptype'] == 'EMO':
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

def vr_solver(ptype, params, rp =[], up = []):
	
	# physical constants
	au_to_Da = 5.48579909065e-4
	au_to_cm = 219474.63067
	a0_to_A = 0.529177210903
	
	# grid point number 
	ngrid = 50000
	
	# reduced mass
	mu = params['mass1'] * params['mass2'] / (params['mass1'] + params['mass2'])
	
	# h^2 / (2*mu) [cm-1 * A^2]
	scale = au_to_Da * au_to_cm * a0_to_A**2 / (2 * mu)
	
	# grid
	step = (params['rmax'] - params['rmin']) / (ngrid - 1)
	r_grid = np.linspace(params['rmin'], params['rmax'], ngrid)
	
	if ptype == 'pw':
		# cubic spline for pec
		spl_pec = splrep(rp, up)
		u_grid = splev(r_grid, spl_pec)
		emax = u_grid[-1]
	elif ptype == 'an':
		if params['ptype'] == 'EMO':
			u_grid = np.array(list(map(lambda x: emo(x, params['de'], params['re'], params['rref'], params['q'], params['beta']), r_grid)))
			emax = params['de']
	else:
		exit(f'ERROR:  Uknown pec type "{ptype}"')
	
	levels = {}
	
	# loop over J to calculate level energies
	for j in range(0, params['jmax'] + 1):
		# 1/R^2
		oneByR2 = r_grid**-2
	
		# diagonal elements (ngrid)
		diagonal = u_grid / scale + j * (j + 1) * oneByR2 + 2 * step**-2
	
		# off-diagonal elements (ngrid-1)
		off_diag = np.full(ngrid - 1, -step**-2)
	
		# SciPy routine to calculate eigenvalues and eigenvectors
		results = eigh_tridiagonal(
			diagonal,
			off_diag,
			select= 'v',
			select_range = (0., emax / scale)
			)
	
		levels[j] = {}
		for v, en in enumerate(results[0]):
			#correction for fd3 scheme
			fd_cor = step**2 / scale / 12 * np.sum((results[1][:, v] * (u_grid - en * scale))**2)
			lev = Level(
				# energy
				en * scale + fd_cor,
				# Bv
				scale * np.sum(results[1][:, v]**2 * oneByR2),
				# grid
				r_grid,
				# WF
				results[1][:, v]
				)
			levels[j][v] = lev
	
	return levels

#=======================================================================
