import requests
import re
requests.packages.urllib3.disable_warnings()

try:
    html = requests.get('https://10.13.0.51/hp/device/InternalPages/Index?id=SuppliesStatus', verify=False).text
except OSError:
    quit()

i = html.find('PagesPrintedWithSupply')
print(re.sub("[^0-9]", "", html[i+24:i+30]))
