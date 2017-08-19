import json
import urllib2
weater_api = '4c8b0d4902e026db02000e3a38e23352'
url = 'http://api.openweathermap.org/data/2.5/weather?q=guntur,in&APPID=4c8b0d4902e026db02000e3a38e23352'
json_obj = urllib2.urlopen(url)
data = json.load(json_obj)
print data
