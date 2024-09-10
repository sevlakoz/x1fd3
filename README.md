# x1fd3

Set of tiny programs to deal with the adiabatic $X^1\Sigma^+$ state of diatomic molecules.

GUI.py - GUI wrapper for all versions

CLI versions:
* pw_pec_approx.py - PEC approximation with EMO function
* level_calc_pw_pec.py - vib.-rot. level calculation for given point-wise PEC
* level_calc_an_pec.py - vib.-rot. level calculation for given analytic PEC
* spectrum_calc_pw_pec.py - vib.-rot. spectrum calculation for given point-wise PEC and point-wise DM
* spectrum_calc_an_pec.py - vib.-rot. spectrum calculation for given analytic PEC and point-wise DM
* fit_pec_to_exp_levels.py - fit analytic PEC to reproduce given exp. vib.-rot. levels


## Usage
```bash
python GUI.py
```
for GUI version

_or_


```bash
python <program> <arguments>
```
for CLI ones.
Run any program without arguments to show help.

