# compare-holidays
Compare the public holidays between two countries

- Main API: https://date.nager.at/api/v3/publicholidays
- Exceptions
  - SA: https://www.gov.za/about-sa/public-holidays
  - UK: https://www.gov.uk/bank-holidays.json

## Quick Example
```Shell
pip install -r requirements.txt
python main.py SA UK
```

Output:
```Txt
Holidays in SA (2022)
- 2022-01-01: New Year’s Day (Saturday)
- 2022-03-21: Human Rights Day
- 2022-04-15: Good Friday
- 2022-04-18: Family Day
- 2022-04-27: Freedom Day
- 2022-05-01: Workers' Day (Sunday)
- 2022-05-02: Public holiday Workers' Day observed
- 2022-06-16: Youth Day
- 2022-08-09: National Women’s Day
- 2022-09-24: Heritage Day (Saturday)
- 2022-12-16: Day of Reconciliation
- 2022-12-25: Christmas Day (Sunday)
- 2022-12-26: Day of Goodwill
------------------------------------------------
Total: 13
Total weekdays: 9

Holidays in UK (2022)
- 2022-01-03: New Year’s Day
- 2022-04-15: Good Friday
- 2022-04-18: Easter Monday
- 2022-05-02: Early May bank holiday
- 2022-06-02: Spring bank holiday
- 2022-06-03: Platinum Jubilee bank holiday
- 2022-08-29: Summer bank holiday
- 2022-12-26: Boxing Day
- 2022-12-27: Christmas Day
- 2023-01-02: New Year’s Day
------------------------------------------------
Total: 10
Total weekdays: 10

.:. SA has 3 more public holiday/s compared to UK
.:. SA has 1 less public holiday/s compared to UK (weekdays only)
```