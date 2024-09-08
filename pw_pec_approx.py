import sys
from cli.classDriver import Driver_pw_pec_approx

driver = Driver_pw_pec_approx(sys.argv[1:])
driver.run()
