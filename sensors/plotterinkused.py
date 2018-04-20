from bs4 import BeautifulSoup
import requests
import re
import json

try:
    html = requests.get("http://10.13.0.52/hp/device/webAccess/index.htm;jsessionid=r0zrwjx0r1?content=usage").text

except OSError:
    quit()

soup = BeautifulSoup(html, "lxml")
table = soup.find("table", attrs={"class":"tablePad3"})

# The first tr contains the field names.

rows = []
for row in table.find_all("tr")[0:]:
    row = (td.get_text() for td in row.find_all("td"))
    rows.append(list(row))

out = (re.sub("[^\d.]+", "", rows[2][1]))
print(out)
