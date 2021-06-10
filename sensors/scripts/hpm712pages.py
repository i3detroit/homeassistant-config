import requests
import re
requests.packages.urllib3.disable_warnings()
try:
    html = requests.get('https://10.13.0.51/hp/device/InternalPages/Index?id=UsagePage', verify=False).text
except OSError:
    quit()
i = html.find('Print.Letter.Total')
print(re.sub("[^0-9]", "", html[i+40:i+48]))
