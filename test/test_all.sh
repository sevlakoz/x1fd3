rm *.log

python -m x1fd3 PecApprox  input/pw_pec.txt                  input/init_emo_params.txt
python -m x1fd3 LevelsPW   input/vr_level_calc_params.txt    input/pw_pec.txt
python -m x1fd3 LevelsAn   input/vr_level_calc_params.txt    input/fitted_emo_params.txt
python -m x1fd3 SpectrumPW input/vr_spectrum_calc_params.txt input/pw_pec.txt            input/pw_dm.txt
python -m x1fd3 SpectrumAn input/vr_spectrum_calc_params.txt input/fitted_emo_params.txt input/pw_dm.txt
python -m x1fd3 FitExp     input/vr_fit_params.txt           input/fitted_emo_params.txt input/pw_pec.txt input/exp_levels.txt

mv PecApprox_1.log  test/PecApprox.ref
mv LevelsPW_1.log   test/LevelsPW.ref
mv LevelsAn_1.log   test/LevelsAn.ref
mv SpectrumPW_1.log test/SpectrumPW.ref
mv SpectrumAn_1.log test/SpectrumAn.ref
mv FitExp_1.log     test/FitExp.ref