#!/bin/bash

rm *.log

python -m x1fd3 GUI input/pw_pec.txt          input/init_emo.txt        PecApprox             run
python -m x1fd3 GUI input/pw_pec.txt          input/params_levels.txt   LevelsPW              run
python -m x1fd3 GUI input/params_levels.txt   input/fitted_emo.txt      LevelsAn              run
python -m x1fd3 GUI input/pw_pec.txt          input/params_spectrum.txt input/pw_dm.txt       SpectrumPW           run
python -m x1fd3 GUI input/params_spectrum.txt input/fitted_emo.txt      input/pw_dm.txt       SpectrumAn           run
python -m x1fd3 GUI input/pw_pec.txt          input/params_fit.txt      input/fitted_emo.txt  input/exp_levels.txt FitExp run

diff PecApprox_GUI_autorun.log  test/PecApprox.ref
diff LevelsPW_GUI_autorun.log   test/LevelsPW.ref
diff LevelsAn_GUI_autorun.log   test/LevelsAn.ref
diff SpectrumPW_GUI_autorun.log test/SpectrumPW.ref
diff SpectrumAn_GUI_autorun.log test/SpectrumAn.ref
diff FitExp_GUI_autorun.log     test/FitExp.ref