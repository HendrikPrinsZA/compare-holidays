#!/usr/bin/env python3

import sys
from classes.holidays import Holidays

holidays = Holidays()

COUNTRY_1 = sys.argv[1]

holidays.importHolidays('NL', yearFrom=2021, yearTo=2023, verbose=False)

# 
# YEAR = 2022
# try:
#   COUNTRY_1 = sys.argv[1]
# except IndexError:
#   print("Missing argument 1, expected country code like 'NL'")
#   exit(0)

# try:
#   COUNTRY_2 = sys.argv[2]
# except IndexError:
#   print("Missing argument 2, expected country code like 'UK'")
#   exit(0)

# summary = holidays.compare(YEAR, COUNTRY_1, COUNTRY_2, verbose=True)