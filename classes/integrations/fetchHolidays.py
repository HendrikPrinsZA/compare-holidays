import re
import requests

from classes.integrations.fetchHolidaysSA import FetchHolidaysSA
from classes.integrations.fetchHolidaysUK import FetchHolidaysUK

class FetchHolidays:
  def get(self, year:int, country:str):
    days = []
    response = requests.get(f"https://date.nager.at/api/v3/publicholidays/{year}/{country}")

    if response.status_code != 200:
      return self.getException(year, country)
    else:
      for entry in response.json():
        days.append({
          "date": entry["date"],
          "title": entry["name"]
        })

    return days

  def getException(self, year:int, country:str):
    if country == "SA":
      return FetchHolidaysSA().get(year)

    if country == "UK":
      return FetchHolidaysUK().get(year)
    
    return None