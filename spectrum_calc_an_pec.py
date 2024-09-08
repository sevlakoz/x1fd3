import sys
from cli import Driver_spectrum_calc_an_pec

driver = Driver_spectrum_calc_an_pec(sys.argv[1:])
driver.run()
