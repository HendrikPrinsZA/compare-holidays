from datetime import datetime
import sys

from loguru import logger

from classes.integrations.fetchHolidays import FetchHolidays
from classes.models.Country import Country
from classes.models.Holiday import Holiday

"""
Compare the public holidays between two countries

- Main API: https://date.nager.at/api/v3/publicholidays
- Exceptions
 - SA: https://www.gov.za/about-sa/public-holidays
 - UK: https://www.gov.uk/bank-holidays.json
"""
class Holidays:

  def getHolidays(self, year:int, countryCode:str, verbose:bool=False):
    days = FetchHolidays().get(year, countryCode)
    total = 0
    totalWeekdays = 0
    for day in days:
      total = total + 1
      date = datetime.strptime(day['date'], "%Y-%m-%d")
      onWeekDay = False
      weekDay = date.__format__("%A")
      if weekDay == "Saturday" or weekDay == "Sunday":
        onWeekDay = True
      else:
        totalWeekdays = totalWeekdays + 1

      if verbose:
        comment = f" ({weekDay})" if onWeekDay else ""
        print(f"- {day['date']}: {day['title']}{comment}")
    
    if verbose:
      print("------------------------------------------------")
      print(f"Total: {total}")
      print(f"Total weekdays: {totalWeekdays}")
    
    return {
      "days": days,
      "total": total,
      "totalWeekdays": totalWeekdays
    }

  def compare(self, year:int, countryCode1:str, countryCode2:str, verbose:bool=False):
    resp = {
      "countryCode1": None,
      "countryCode2": None,
      "notes": []
    }

    msg = f"Holidays in {countryCode1} ({year})"
    resp["notes"].append(msg)
    if verbose:
      print(msg)

    resp["countryCode1"] = self.getHolidays(year, countryCode1, verbose)

    msg = f"\nHolidays in {countryCode2} ({year})"
    resp["notes"].append(msg)
    if verbose:
      print(msg)
      
    resp["countryCode2"] = self.getHolidays(year, countryCode2, verbose)

    diffTotal = resp["countryCode1"]["total"] - resp["countryCode2"]["total"]
    resp["diffTotal"] = diffTotal
    lessMore = f"{abs(diffTotal)} {'less' if diffTotal < 0 else 'equal' if {diffTotal} == 0 else 'more'}"
    description = f".:. {countryCode1} has {lessMore} public holiday/s compared to {countryCode2}"
    resp["notes"].append(description)
    if verbose:
      print(f"\n{description}")

    diffWeekdays = resp["countryCode1"]["totalWeekdays"] - resp["countryCode2"]["totalWeekdays"]
    resp["diffWeekdays"] = diffWeekdays
    
    lessMore = f"{abs(diffWeekdays)} {'less' if diffWeekdays < 0 else 'equal' if {diffWeekdays} == 0 else 'more'}"
    description = f".:. {countryCode1} has {lessMore} public holiday/s compared to {countryCode2} (weekdays only)"
    resp["notes"].append(description)
    if verbose:
      print(f"{description}")

    return resp

  def importHolidays(self, countryCode:str, yearFrom:int, yearTo:int, verbose:bool):
    country = Country.firstWhere('code', countryCode)

    if country is None:
      logger.error(f"Unable to find country by code: '{countryCode}'")
      sys.exit()

    print("Country...")
    print(country)

    for year in range(yearFrom, (yearTo + 1)):
      days = self.getHolidays(year, countryCode, verbose)
      for day in days['days']:
        print(day)
        holiday = Holiday.updateOrCreate({
          'country_id': country['id']
        })
        # holiday = Holiday.updateOrCreate({
        #   'country_id': country['id'],
        #   'date': day['date'],
        #   'title': day['title']
        # })
        