import sys
from cli import DriverFitExp

driver = DriverFitExp(sys.argv[1:])
driver.run()
