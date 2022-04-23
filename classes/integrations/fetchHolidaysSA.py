import re
import requests
from bs4 import BeautifulSoup
from datetime import datetime

class FetchHolidaysSA:
  def get(self, year:int):
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