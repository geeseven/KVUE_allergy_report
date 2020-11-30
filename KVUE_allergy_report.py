#!/usr/bin/env python

from datetime import date

from bs4 import BeautifulSoup
from rich import box
from rich.console import Console
from rich.table import Table
from selenium import webdriver

# iframe from https://www.kvue.com/allergy
url = "https://www.keepandshare.com/calendar/show_month.php?i=1940971"

logLocation = "/dev/null"
# For debugging
# logLocation = "./geckodriver.log"
opts = webdriver.FirefoxOptions()
opts.headless = True
brower = webdriver.Firefox(options=opts, service_log_path=logLocation)

brower.get(url)
soup = BeautifulSoup(brower.page_source, "html.parser")
brower.close()

# the background color for today is a different color than all other days
allergyReport = soup.find("span", {"style": "background-color: #ffffff;"})

# KVUE has allergy reports almost everyday
# maybe figure out how to get the most recent report instead of just today
if not allergyReport:
    print(
        "KVUE does not have an allergy report today."
        "For recent reports, check {}".format(url)
    )
    exit()

# sometime the allery report ends with a ".", lets remove it & spilt the report
if allergyReport.text[-1] == ".":
    allergies = allergyReport.text[0:-1].split(", ")
else:
    allergies = allergyReport.text.split(", ")

table = Table(
    border_style="dim green",
    box=box.SIMPLE_HEAD,
    header_style="white",
    title="KVUE allergy report for {}".format(date.today()),
)
table.add_column("allergen", style="dim")
table.add_column("severity", style="dim")

for item in sorted(allergies):
    # change formatting from 'Trees 13 gr/m3 Low' to ['Trees', '13 gr/m3 Low']
    i = item.split(" ", 1)
    table.add_row(i[0], i[1])

Console().print(table)
