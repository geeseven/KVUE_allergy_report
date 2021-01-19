#!/usr/bin/env python

from datetime import datetime, timedelta
from re import split
from unicodedata import normalize

from bs4 import BeautifulSoup
from rich import box
from rich.console import Console
from rich.table import Table
from selenium import webdriver

# iframe from https://www.kvue.com/allergy
base_url = "https://www.keepandshare.com/calendar/show_month.php?i=1940971&vw=day&date="  # noqa:


def screenscrap(url):
    logLocation = "/dev/null"
    # For debugging
    # logLocation = "./geckodriver.log"
    opts = webdriver.FirefoxOptions()
    opts.headless = True
    browser = webdriver.Firefox(options=opts, service_log_path=logLocation)
    browser.get(url)
    soup = BeautifulSoup(browser.page_source, "html.parser")
    browser.close()
    return soup


date = datetime.now()

# starting with today, check if there is a report, if not find the most recent
count = 1
while True:
    if count == 5:
        print("ERROR, can't connect or get a report after 5 tries")
        exit(1)
    html = screenscrap(base_url + date.strftime("%Y-%m-%d"))
    allergyReport = html.find("div", {"class": "calendar_one_line_text"})
    if not allergyReport:
        date = date - timedelta(days=1)
        count += 1
    else:
        break

# clean up results
# sometime the report ends with a ".", lets remove it
allergies = allergyReport.text.strip(".")
# fix encoding like \xa0 https://stackoverflow.com/a/34669482
allergies = normalize("NFKD", allergies)
# spilt for each allergen and remove leading spaces
allergies = [x.lstrip() for x in split(", |; ", allergies)]

table = Table(
    border_style="dim green",
    box=box.SIMPLE_HEAD,
    header_style="white",
    title="KVUE allergy report from {}".format(date.strftime("%B %d, %Y")),
)
table.add_column("allergen", style="dim")
table.add_column("severity", style="dim")

for item in sorted(allergies):
    # change formatting from 'Trees 13 gr/m3 Low' to ['Trees', '13 gr/m3 Low']
    i = item.split(" ", 1)
    table.add_row(i[0], i[1])

Console().print(table)
