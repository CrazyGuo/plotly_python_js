import clr
import sys

sys.path.append("C:\Works\odoo_project\plotly_python_js\FFTester")
clr.FindAssembly("FFTester.dll")

from FFTester import *


sample = Tester()

Tester.getStation()
