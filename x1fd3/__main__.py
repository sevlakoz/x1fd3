from argparse import ArgumentParser

from x1fd3.cli import DriverPecApprox
from x1fd3.cli import DriverLevelsPW
from x1fd3.cli import DriverLevelsAn
from x1fd3.cli import DriverSpectrumPW
from x1fd3.cli import DriverSpectrumAn
from x1fd3.cli import DriverFitExp


parser = ArgumentParser()

parser.add_argument(
    'mode',
    help = 'run mode',
    choices = ['GUI', 'PecApprox', 'LevelsPW', 'LevelsAn', 'SpectrumPW', 'SpectrumAn', 'ExpFit']
)

parser.add_argument(
    'input_files',
    help = 'input files for CLI-based modes',
    nargs = '*'
)

args = parser.parse_args()


if args.mode == 'GUI':
    from x1fd3.gui import MainWindow
    main_window = MainWindow()
    main_window.root.mainloop()
else:
    match args.mode:
        case 'PecApprox':
            driver = DriverPecApprox(args.input_files)
        case 'LevelsPW':
            driver = DriverLevelsPW(args.input_files) #type: ignore
        case 'LevelsAn':
            driver = DriverLevelsAn(args.input_files) #type: ignore
        case 'SpectrumPW':
            driver = DriverSpectrumPW(args.input_files) #type: ignore
        case 'SpectrumAn':
            driver = DriverSpectrumAn(args.input_files) #type: ignore
        case 'FitExp':
            driver = DriverFitExp(args.input_files) #type: ignore
    driver.run()
