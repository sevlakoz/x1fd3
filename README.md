# x1fd3

Set of tiny programs to deal with the adiabatic $X^1\Sigma^+$ state of diatomic molecules.

## Usage
```bash
python -m x1fd3 mode [input files]
```
Available modes:
* GUI - TK wrapper for all other modes 
* PecApprox - PEC approximation with EMO function 
* LevelsPW - vib.-rot. level calculation for given point-wise PEC
* LevelsAn - vib.-rot. level calculation for given analytic PEC
* SpectrumPW - vib.-rot. spectrum calculation for given point-wise PEC and point-wise DM
* SpectrumAn - vib.-rot. spectrum calculation for given analytic PEC and point-wise DM
* ExpFit - fit analytic PEC to reproduce given exp. vib.-rot. levels

## Requirements
* python >= 3.10
* numpy
* scipy
* tkinter