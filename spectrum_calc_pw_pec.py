import sys
from cli import DriverSpectrumPW

driver = DriverSpectrumPW(sys.argv[1:])
driver.run()
