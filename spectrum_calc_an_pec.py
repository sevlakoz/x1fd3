import sys
from cli.classDriver import Driver_spectrum_calc_an_pec

driver = Driver_spectrum_calc_an_pec(sys.argv[1:])
driver.run()
