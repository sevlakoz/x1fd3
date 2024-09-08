import sys
from cli.classDriver import Driver_fit_pec_to_exp_levels

driver = Driver_fit_pec_to_exp_levels(sys.argv[1:])
driver.run()
