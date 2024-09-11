import sys

from x1fd3.cli import DriverPecApprox
from x1fd3.cli import DriverLevelsPW
from x1fd3.cli import DriverLevelsAn
from x1fd3.cli import DriverSpectrumPW
from x1fd3.cli import DriverSpectrumAn
from x1fd3.cli import DriverFitExp

mode_av = 'Available modes:\n' +\
          '    GUI\n' +\
          '    PecApprox\n' +\
          '    LevelsPW\n' +\
          '    LevelsAn\n' +\
          '    SpectrumPW\n' +\
          '    SpectrumAn\n' +\
          '    ExpFit'

if len(sys.argv) < 2:
    raise RuntimeError(
        'Missing command line argument: mode\n' +\
        mode_av
    )
else:
    mode = sys.argv[1]
    inp_files = sys.argv[2:]



if mode == 'GUI':
    from x1fd3.gui import MainWindow # import here to remove tk dependancy for CLI version
    main_window = MainWindow()
    main_window.root.mainloop()
else:
    if mode == 'PecApprox':
        driver = DriverPecApprox(inp_files)
    elif mode == 'LevelsPW':
        driver = DriverLevelsPW(inp_files) #type: ignore
    elif mode == 'LevelsAn':
        driver = DriverLevelsAn(inp_files) #type: ignore
    elif mode == 'SpectrumPW':
        driver = DriverSpectrumPW(inp_files) #type: ignore
    elif mode == 'SpectrumAn':
        driver = DriverSpectrumAn(inp_files) #type: ignore
    elif mode == 'FitExp':
        driver = DriverFitExp(inp_files) #type: ignore
    else:
        raise RuntimeError(
            'Wrong first command line argument (mode)\n' +\
            mode_av
        )
    driver.run()
