import requests

URL = 'http://dataservice.accuweather.com/locations/v1/regions'
data = requests.get(URL)
datas = list()
for element in data: #iteramos sobre data
    datas.append(element)
print(datas)