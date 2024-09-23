#!/bin/bash

rm *.log

python -m x1fd3 GUI autorun PecApprox  input/init_emo.txt        input/pw_pec.txt
python -m x1fd3 GUI autorun LevelsPW   input/params_levels.txt   input/pw_pec.txt
python -m x1fd3 GUI autorun LevelsAn   input/params_levels.txt   input/fitted_emo.txt
python -m x1fd3 GUI autorun SpectrumPW input/params_spectrum.txt input/pw_pec.txt     input/pw_dm.txt
python -m x1fd3 GUI autorun SpectrumAn input/params_spectrum.txt input/fitted_emo.txt input/pw_dm.txt
python -m x1fd3 GUI autorun FitExp     input/params_fit.txt      input/fitted_emo.txt input/pw_pec.txt input/exp_levels.txt

diff PecApprox_GUI_autorun.log  test/PecApprox.ref
diff LevelsPW_GUI_autorun.log   test/LevelsPW.ref
diff LevelsAn_GUI_autorun.log   test/LevelsAn.ref
diff SpectrumPW_GUI_autorun.log test/SpectrumPW.ref
diff SpectrumAn_GUI_autorun.log test/SpectrumAn.ref
diff FitExp_GUI_autorun.log     test/FitExp.ref
