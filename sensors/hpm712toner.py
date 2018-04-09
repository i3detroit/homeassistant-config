import requests
import re
requests.packages.urllib3.disable_warnings()
html = requests.get('http://10.13.0.51', verify=False).text
i = html.find('PLR0')
print(re.sub("[^0-9]", "", html[i+18:i+21]))
