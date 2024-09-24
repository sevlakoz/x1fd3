# x1fd3

A program to deal with the adiabatic $X^1\Sigma^+$ state of diatomic molecules.

## Requirements
* python >= 3.10
* numpy
* scipy
* tkinter

## Test
On *nix systems run 
```bash
test/test.sh test
```

Note that last test could fail since it's slightly system-dependent.
If "PEC fit done:" is in "FitExp_1.log" it works just fine.

## Usage
```bash
python -m x1fd3 [mode] [*input files*]
```
Available modes:
* GUI - TK wrapper for all other modes
* PecApprox - Potential energy curve (PEC) approximation with analytic function 
* LevelsPW - Vibrational-rotational level calculation for given point-wise PEC
* LevelsAn - Vibrational-rotational level calculation for given analytic PEC
* SpectrumPW - Vibrational-rotational spectrum calculation for given point-wise PEC and point-wise dipole moment (DM)
* SpectrumAn - Vibrational-rotational spectrum calculation for given analytic PEC and point-wise DM
* FitExp - fit analytic PEC to reproduce given experimental vibrational-rotational levels

No input files required to run GUI. 
For CLI-based modes 2, 3, or 4 files need to be provided.
Run any of these modes without no arguments to see help.

## Mode details

### PecApprox
Point-wise PEC is approximated with Extended Morse Oscillator (EMO) function:
```math
U_{EMO} = D_e  \left( 1 - e^{-\beta(R) \cdot (R-R_e)} \right)^2 
```
where
```math
\beta(R) = \sum_{i=0}^N \beta_i \cdot y^i 
```
and
```math
y = \frac{R^q - R_{ref}^q}{R^q + R_{ref}^q}
```
$`D_e`$, $`R_e`$ and $`\beta_0`$, ..., $`\beta_N`$ are optimized within non-linear least squares.

Note: MLR and DELR are available as well.

### LevelsPW
Vibrational-rotational levels are found by solving the radial Schrodinger equation:
```math
\left[-\frac{\hbar^2}{2\mu}\frac{d2}{dR^2} + U(R) + \frac{\hbar^2 J(J+1)}{2\mu R^2}\right]\Psi_v = E\Psi_v
```
The finite-difference scheme is used within the scheme 3-point approximation of 2nd derivative:
```math
f''(x_i) \approx \frac{ f(x_{i-1}) - 2f(x_i) + f(x_{i+1}) }{ \Delta x^2}
```
Within this method the original differential equation is transformed to tridiagonal symmetric matrix eigenvalue problem.

PEC ($`U(R)`$) is required in point-wise format, spline interpolation is used.

### LevelsAn
Similar to **LevelsPW**, but with analytic (EMO, etc) representation of PEC.

### SpectrumPW
**LevelsPW** with additional matrix elements calculation for given point-wise DM ($`D(R)`$) and lower and upper vibrational quantum numbers $`v_1`$ and $`v_2`$:
```math
\mu = <\Psi_{v1}|D|\Psi_{v2}>
```
Total transition matrix elements for absorption and emission spectra can be estimated as:
```math
M^2 = \mu^2 \cdot S
```
where $`S`$ are Hoenl-London factors.

### SpectrumAn
Similar to **SpectrumPW**, but with analytic (EMO, etc) representation of PEC.


### FitExp
PEC is optimized to fit given set of vibrational-rotational experimental levels.
Least-squares procedure is based on Hellmann–Feynman theorem:
```math
\frac{\partial E}{\partial p_i} = 
\left< \Psi_v 
\middle | 
\frac{\partial U(p_1,p_2,...) }{\partial p_i} 
\middle | 
\Psi_v \right >
```
where $`p_i`$ are $`D_e`$, $`R_e`$ and $`\beta_0`$, ..., $`\beta_N`$.
