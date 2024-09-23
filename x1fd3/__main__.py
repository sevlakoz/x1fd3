import traceback
from argparse import ArgumentParser
from time import time

from x1fd3.base import Logger
from x1fd3.cli import DriverPecApprox, \
                      DriverLevelsPW, \
                      DriverLevelsAn, \
                      DriverSpectrumPW, \
                      DriverSpectrumAn, \
                      DriverFitExp
from x1fd3.gui import MainWindow

parser = ArgumentParser()

parser.add_argument(
    'mode',
    help = 'run mode',
    choices = ['GUI', 'PecApprox', 'LevelsPW', 'LevelsAn', 'SpectrumPW', 'SpectrumAn', 'FitExp']
)

parser.add_argument(
    'input_files',
    help = 'input files for CLI-based modes',
    nargs = '*'
)

args = parser.parse_args()


if args.mode == 'GUI':
    main_window = MainWindow(args.input_files)
    main_window.root.mainloop()
else:
    out = Logger(args.mode)

    start = time()

    try:
        match args.mode:
            case 'PecApprox':
                DriverPecApprox(args.input_files, out).run()
            case 'LevelsPW':
                DriverLevelsPW(args.input_files, out).run()
            case 'LevelsAn':
                DriverLevelsAn(args.input_files, out).run()
            case 'SpectrumPW':
                DriverSpectrumPW(args.input_files, out).run()
            case 'SpectrumAn':
                DriverSpectrumAn(args.input_files, out).run()
            case 'FitExp':
                DriverFitExp(args.input_files, out).run()
        print('Success!')
    except BaseException: # pylint: disable = W0718
        err = traceback.format_exc() # pylint: disable=C0103
        print('Error!')
        print(err)
        out.print(err)

    finish = time()

    print(f'Execution time, s: {finish - start:.3f}')
    print(f'Results stored in {out.fname}')
