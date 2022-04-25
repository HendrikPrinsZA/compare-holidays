#!/usr/bin/env python3

"""
Cowboying!

Messing around with finding stats from holidays
- Import holidays into database
- Compare countries globally
"""
from classes.holidays import Holidays

holidays = Holidays()

COUNTRY_1 = 'NL'
holidays.importHolidays('NL', yearFrom=1900, yearTo=2030, verbose=False)