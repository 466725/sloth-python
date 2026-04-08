import requests
import re

url = "https://www.weather.com.cn/weather1d/101010100.shtml"
"""
    <span class="name">九寨沟</span>
    <span class="weather">多云转小雨</span>
    <span class="wd">10/23℃</span>
    <span class="zs">适宜</span>
"""
response = requests.get(url)
response.encoding = 'utf-8'
# print(response.text)

location = re.findall('<span class="name">([\u4e00-\u9fa5]*)</span>', response.text)
weather = re.findall('<span class="weather">([\u4e00-\u9fa5]*)</span>', response.text)
temperature = re.findall('<span class="wd">(.*)</span>', response.text)
outdoor_wellbeing = re.findall('<span class="zs">([\u4e00-\u9fa5]*)</span>', response.text)
# print(location)
# print(weather)
# print(temperature)
# print(outdoor_wellbeing)

zip_list = []
for a, b, c, d in zip(location, weather, temperature, outdoor_wellbeing):
    zip_list.append([a, b, c, d])

for item in zip_list:
    print(item)

# Same thing, different approach
response = requests.get(url, timeout=10)
response.encoding = "utf-8"
html = response.text

# Regex patterns
pattern_name = r'<span class="name">([\u4e00-\u9fa5]+)</span>'
pattern_weather = r'<span class="weather">([\u4e00-\u9fa5]+)</span>'
pattern_temp = r'<span class="wd">(.*?)</span>'
pattern_zs = r'<span class="zs">([\u4e00-\u9fa5]+)</span>'

location = re.findall(pattern_name, html)
weather = re.findall(pattern_weather, html)
temperature = re.findall(pattern_temp, html)
outdoor_wellbeing = re.findall(pattern_zs, html)

# Combine results
results = list(zip(location, weather, temperature, outdoor_wellbeing))

for item in results:
    print(item)
