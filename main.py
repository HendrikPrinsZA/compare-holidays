#!/usr/bin/env python3

"""
Compare the public holidays between two countries

- Main API: https://date.nager.at/api/v3/publicholidays
- Exceptions
 - SA: https://www.gov.za/about-sa/public-holidays
 - UK: https://www.gov.uk/bank-holidays.json
"""

import re
import requests
import sys
from bs4 import BeautifulSoup
from datetime import datetime

def getPublicHolidays(year, country):
  days = []
  response = requests.get(f"https://date.nager.at/api/v3/publicholidays/{year}/{country}")

  if response.status_code != 200:
    return getPublicHolidaysException(year, country)
  else:
    for entry in response.json():
      days.append({
        "date": entry["date"],
        "title": entry["name"]
      })

  return days

def getPublicHolidaysException(year, country):
  if country == "SA":
    return getPublicHolidaysExceptionSA(year)

  if country == "UK":
    return getPublicHolidaysExceptionUK(year)
  
  return None

def getPublicHolidaysExceptionSA(year):
  days = []
  response = requests.get(f"https://www.gov.za/about-sa/public-holidays")

  if response.status_code != 200:
    return None

  soup = BeautifulSoup(response.content, "html.parser")
  pars = soup.findAll("p")
  
  for par in pars:
    lines = par.get_text(strip=True, separator='\n').splitlines()

    shouldBreak = False
    for line in lines:
      line = line.replace("\xa0", " ")
      parts = re.split(" |:", line)

      if len(parts) < 2:
        continue

      day = parts[0]

      if not day.isnumeric():
        continue

      month = parts[1]
      title = " ".join(parts[3:])

      date = datetime.strptime(f"{year}-{month}-{day}", "%Y-%B-%d")
      dateString = date.__format__("%Y-%m-%d")

      foundDate = False
      for item in days:
        if item.get("date") == dateString:
          foundDate = True
          break
      
      if foundDate == True:
        shouldBreak = True
        break

      days.append({
        "date": dateString,
        "title": title
      })

    if shouldBreak:
      return days

  return None

def getPublicHolidaysExceptionUK(year):
  days = []
  response = requests.get(f"https://www.gov.uk/bank-holidays.json")

  if response.status_code != 200:
    return None
  else:
    for event in response.json()['england-and-wales']['events']:
      date = datetime.strptime(f"{event['date']}", "%Y-%m-%d")

      if int(date.__format__("%Y")) < year:
        continue

      days.append(event)

      if int(date.__format__("%Y")) > year:
        break
    
    return days


def getHolidays(year, country, verbose=False):
  days = getPublicHolidays(year, country)
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

    comment = f" ({weekDay})" if onWeekDay else ""
    if verbose:
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

def getSummmary(year, country1, country2, verbose):
  resp = {
    "country1": None,
    "country2": None,
    "notes": []
  }

  msg = f"Holidays in {country1} ({year})"
  resp["notes"].append(msg)
  if verbose:
    print(msg)

  resp["country1"] = getHolidays(year, country1, verbose)

  msg = f"\nHolidays in {country2} ({year})"
  resp["notes"].append(msg)
  if verbose:
    print(msg)
    
  resp["country2"] = getHolidays(year, country2, verbose)

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

YEAR = 2022

try:
  COUNTRY_1 = sys.argv[1]
except IndexError:
  print("Missing argument 1, expected country code like 'NL'")
  exit(0)

try:
  COUNTRY_2 = sys.argv[2]
except IndexError:
  print("Missing argument 2, expected country code like 'UK'")
  exit(0)

summary = getSummmary(YEAR, COUNTRY_1, COUNTRY_2, verbose=True)
