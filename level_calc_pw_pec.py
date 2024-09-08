import sys
from cli.classDriver import Driver_level_calc_pw_pec

driver = Driver_level_calc_pw_pec(sys.argv[1:])
driver.run()
