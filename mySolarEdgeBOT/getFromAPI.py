import requests
from config import  MY_SOLAR_EDGE_SITE, API_KEY

url = 'https://monitoringapi.solaredge.com/site/{}/currentPowerFlow?api_key={}'.format(MY_SOLAR_EDGE_SITE, API_KEY)
responseJsonBody = requests.get(url).json()

sun = responseJsonBody.get('siteCurrentPowerFlow').get('PV')
battery = responseJsonBody.get('siteCurrentPowerFlow').get('STORAGE')

print('SUN: {}'.format(sun))
print('BATTERY: {}'.format(battery))

print(responseJsonBody)