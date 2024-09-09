import sys
from cli import DriverPecApprox

driver = DriverPecApprox(sys.argv[1:])
driver.run()
