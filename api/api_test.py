import requests

url = "https://connect.cineplex.com/ClientServices/CineplexClientServicesWeb/CreateApplicationSession"

payload = "{\n\t\"ApplicationKey\": \"9fbcb70c-8bcd-43eb-930f-d99968b4561e\"\n}"
print(payload)
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'visid_incap_2293254=KmLrzNVaTjaHg3x0G3Oy953cx14AAAAAQUIPAAAAAABnm269Hcp0OlaqxUdlwgYy; '
              'visid_incap_2306869=JoBxgYSPS1m5GqKMDpJgkqjcx14AAAAAQUIPAAAAAABn0Gmpm3WgBe58qDpIGef3; '
              'Cineplex MVC Sandbox_Language=en-us; '
              'visid_incap_2293438=4gPNBHNoSyuMZb0cLC/Xl0RnGV8AAAAAQUIPAAAAAABEKGzC2rm/wMrgFLU9xEiB; '
              'visid_incap_2293416=yX7BaoyFTMaYGavMvjoxsVVnGV8AAAAAQUIPAAAAAADyxbSa8vzqW1TZlzesE4+a; '
              'citrix_ns_id_.cineplex.com_%2F_wlf=AAAAAAWxXXn9LUirf5VeOWNKdIyPLW7-INZb8X8XbfIy8yinxAZmj4B0NsseBBMetPRT5da-SyP0lavvhLADPAEjj0_sImUu41DhNYVDsVwEAKrKug==&'
}
response = requests.request("POST", url, headers = headers, data = payload)
responseJson = response.json()
print(responseJson)
SessionTokenExpires = responseJson['SessionTokenExpires']
assert response.status_code == 200
