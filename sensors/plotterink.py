from bs4 import BeautifulSoup
import requests
import re
import json

try:
    html = requests.get("http://10.13.0.52/hp/device/webAccess/index.htm").text

except OSError:
    print("Connection Error. Plotter is probably turned off.")
    quit()

i = html.find('Buy paper now')

html = html[i:i+5000]

soup = BeautifulSoup(html, "lxml")
table = soup.find("table", attrs={"class":"dataTable"})

# The first tr contains the field names.
headings = [th.get_text() for th in table.find("tr").find_all("th")]

datasets = []
for row in table.find_all("tr")[1:]:
    dataset = zip(headings, (td.get_text() for td in row.find_all("td")))
    datasets.append(list(dataset))

out = {}

for x in datasets:
    a = int(re.sub("[^0-9]", "", x[3][1])) / int(re.sub("[^0-9]", "", x[4][1]))
    out[re.sub(" ", "_", x[1][1])] =  round(100*a)

print(json.dumps(out))
