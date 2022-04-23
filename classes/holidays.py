from datetime import datetime

from classes.integrations.fetchHolidays import FetchHolidays

"""
Compare the public holidays between two countries

- Main API: https://date.nager.at/api/v3/publicholidays
- Exceptions
 - SA: https://www.gov.za/about-sa/public-holidays
 - UK: https://www.gov.uk/bank-holidays.json
"""
class Holidays:
  def getHolidays(self, year:int, country:str, verbose:bool=False):
    days = FetchHolidays().get(year, country)
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

  def compare(self, year:int, country1:str, country2:str, verbose:bool=False):
    resp = {
      "country1": None,
      "country2": None,
      "notes": []
    }

    msg = f"Holidays in {country1} ({year})"
    resp["notes"].append(msg)
    if verbose:
      print(msg)

    resp["country1"] = self.getHolidays(year, country1, verbose)

    msg = f"\nHolidays in {country2} ({year})"
    resp["notes"].append(msg)
    if verbose:
      print(msg)
      
    resp["country2"] = self.getHolidays(year, country2, verbose)

    diffTotal = resp["country1"]["total"] - resp["country2"]["total"]
    resp["diffTotal"] = diffTotal
    lessMore = f"{abs(diffTotal)} {'less' if diffTotal < 0 else 'equal' if {diffTotal} == 0 else 'more'}"
    description = f".:. {country1} has {lessMore} public holiday/s compared to {country2}"
    resp["notes"].append(description)
    if verbose:
      print(f"\n{description}")

    diffWeekdays = resp["country1"]["totalWeekdays"] - resp["country2"]["totalWeekdays"]
    resp["diffWeekdays"] = diffWeekdays
    
    lessMore = f"{abs(diffWeekdays)} {'less' if diffWeekdays < 0 else 'equal' if {diffWeekdays} == 0 else 'more'}"
    description = f".:. {country1} has {lessMore} public holiday/s compared to {country2} (weekdays only)"
    resp["notes"].append(description)
    if verbose:
      print(f"{description}")

    return resp