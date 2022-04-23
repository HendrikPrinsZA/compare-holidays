import requests
from datetime import datetime

class FetchHolidaysUK:
  def get(self, year:int):
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