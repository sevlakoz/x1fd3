import sys
from cli import DriverSpectrumAn

driver = DriverSpectrumAn(sys.argv[1:])
driver.run()
