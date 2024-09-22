#!/bin/bash

if [ -n "$1" ] && [ "$1" == "make" ]; then
    CMD="mv"
elif [ -n "$1" ] && [ "$1" == "test" ]; then
    CMD="diff"
else
    echo "set \$1: "
    echo "\"make\" - update test/*.ref"
    echo "\"test\" - compare results to test/*.ref"
    exit 1
fi

rm *.log

python -m x1fd3 PecApprox  input/pw_pec.txt          input/init_emo.txt
python -m x1fd3 LevelsPW   input/params_levels.txt   input/pw_pec.txt
python -m x1fd3 LevelsAn   input/params_levels.txt   input/fitted_emo.txt
python -m x1fd3 SpectrumPW input/params_spectrum.txt input/pw_pec.txt     input/pw_dm.txt
python -m x1fd3 SpectrumAn input/params_spectrum.txt input/fitted_emo.txt input/pw_dm.txt
python -m x1fd3 FitExp     input/params_fit.txt      input/fitted_emo.txt input/pw_pec.txt input/exp_levels.txt

$CMD PecApprox_1.log  test/PecApprox.ref
$CMD LevelsPW_1.log   test/LevelsPW.ref
$CMD LevelsAn_1.log   test/LevelsAn.ref
$CMD SpectrumPW_1.log test/SpectrumPW.ref
$CMD SpectrumAn_1.log test/SpectrumAn.ref
$CMD FitExp_1.log     test/FitExp.ref
