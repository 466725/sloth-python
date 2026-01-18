import requests

url = "https://connect.cineplex.com/ClientServices/CineplexClientServicesWeb/CreateApplicationSession"

payload = "{\n\t\"ApplicationKey\": \"9fbcb70c-8bcd-43eb-930f-d99968b4561e\"\n}"
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'visid_incap_2293254=KmLrzNVaTjaHg3x0G3Oy953cx14AAAAAQUIPAAAAAABnm269Hcp0OlaqxUdlwgYy; visid_incap_2306869=JoBxgYSPS1m5GqKMDpJgkqjcx14AAAAAQUIPAAAAAABn0Gmpm3WgBe58qDpIGef3; visid_incap_2306868=W9I230B7QDeWMjMUg2QR030ByF4AAAAAQUIPAAAAAADGg+fMEPqM6rXTYvo0Mfk8; visid_incap_2293204=9b3XTP8jRraMxObWM7PcQx8CyF4AAAAAQUIPAAAAAACLBn0TU4K63yJrGsR7uVTa; visid_incap_2293405=+Q51jhsrRTyhyAuqplymIrSW7F4AAAAAQUIPAAAAAABkisJ8OZVlYuRXdgfD648x; visid_incap_2320540=ZMfcd64QT3qKpFjyos4UBLLK7F4AAAAAQUIPAAAAAABpGQB/Mp3s83qE3npKy6FZ; visid_incap_2293202=cLiM/gy/Qs6vjDnpZlcCVXLADV8AAAAAQUIPAAAAAADFARmhPxORGyNeiIV0qUu8; visid_incap_2293381=WFIasLg2SSawzTtb70PmEFPZDl8AAAAAQUIPAAAAAAANRsm6oVGQTHObi8pNYqb3; visid_incap_2293368=RYrS36J+Tq2mlLMEbp9aNuWsEV8AAAAAQUIPAAAAAABuITetcFCzSOviCiGSvRIt; visid_incap_2350392=XxF++V0lT7aC2astotooGqoQGF8AAAAAQUIPAAAAAACE6wkCROuSp34YsLKRZNKB; visid_incap_2293377=GbBCpkEWSyeZeENwFRB7nK0QGF8AAAAAQUIPAAAAAACc6sN3crxeuBIx/bwZckwC; Cineplex MVC Sandbox_Language=en-us; visid_incap_2293438=4gPNBHNoSyuMZb0cLC/Xl0RnGV8AAAAAQUIPAAAAAABEKGzC2rm/wMrgFLU9xEiB; visid_incap_2293416=yX7BaoyFTMaYGavMvjoxsVVnGV8AAAAAQUIPAAAAAADyxbSa8vzqW1TZlzesE4+a; citrix_ns_id_.cineplex.com_%2F_wlf=AAAAAAWxXXn9LUirf5VeOWNKdIyPLW7-INZb8X8XbfIy8yinxAZmj4B0NsseBBMetPRT5da-SyP0lavvhLADPAEjj0_sImUu41DhNYVDsVwEAKrKug==&'
}
r = requests.request("POST", url, headers=headers, data=payload)
response = r.json()
Message = response['Result']['Status']
SessionToken = response['SessionToken']
SessionTokenExpires = response['SessionTokenExpires']
assert r.status_code == 200
assert response['Result']['Status'] == 1

url = "https://connect.cineplex.com/ClientServices/CineplexClientServicesWeb/Login"

payload = '{\n    \"SessionToken\": \"' + str(
    SessionToken) + '\",\n    \"Password\": \"Cineplex123\",\n    \"Email\": \"cineplex.test@gmail.com\",\n    \"Source\": \"1\",\n    \"LanguageType\": \"1\"\n}'
headers = {
    'Content-Type': 'application/json',
    'Cookie': 'visid_incap_2293254=KmLrzNVaTjaHg3x0G3Oy953cx14AAAAAQUIPAAAAAABnm269Hcp0OlaqxUdlwgYy; visid_incap_2306869=JoBxgYSPS1m5GqKMDpJgkqjcx14AAAAAQUIPAAAAAABn0Gmpm3WgBe58qDpIGef3; visid_incap_2306868=W9I230B7QDeWMjMUg2QR030ByF4AAAAAQUIPAAAAAADGg+fMEPqM6rXTYvo0Mfk8; visid_incap_2293204=9b3XTP8jRraMxObWM7PcQx8CyF4AAAAAQUIPAAAAAACLBn0TU4K63yJrGsR7uVTa; visid_incap_2293405=+Q51jhsrRTyhyAuqplymIrSW7F4AAAAAQUIPAAAAAABkisJ8OZVlYuRXdgfD648x; visid_incap_2320540=ZMfcd64QT3qKpFjyos4UBLLK7F4AAAAAQUIPAAAAAABpGQB/Mp3s83qE3npKy6FZ; visid_incap_2293202=cLiM/gy/Qs6vjDnpZlcCVXLADV8AAAAAQUIPAAAAAADFARmhPxORGyNeiIV0qUu8; visid_incap_2293381=WFIasLg2SSawzTtb70PmEFPZDl8AAAAAQUIPAAAAAAANRsm6oVGQTHObi8pNYqb3; visid_incap_2293368=RYrS36J+Tq2mlLMEbp9aNuWsEV8AAAAAQUIPAAAAAABuITetcFCzSOviCiGSvRIt; visid_incap_2350392=XxF++V0lT7aC2astotooGqoQGF8AAAAAQUIPAAAAAACE6wkCROuSp34YsLKRZNKB; visid_incap_2293377=GbBCpkEWSyeZeENwFRB7nK0QGF8AAAAAQUIPAAAAAACc6sN3crxeuBIx/bwZckwC; Cineplex MVC Sandbox_Language=en-us; visid_incap_2293438=4gPNBHNoSyuMZb0cLC/Xl0RnGV8AAAAAQUIPAAAAAABEKGzC2rm/wMrgFLU9xEiB; visid_incap_2293416=yX7BaoyFTMaYGavMvjoxsVVnGV8AAAAAQUIPAAAAAADyxbSa8vzqW1TZlzesE4+a; citrix_ns_id_.cineplex.com_%2F_wlf=AAAAAAWxXXn9LUirf5VeOWNKdIyPLW7-INZb8X8XbfIy8yinxAZmj4B0NsseBBMetPRT5da-SyP0lavvhLADPAEjj0_sImUu41DhNYVDsVwEAKrKug==&'
}
print(payload)
r = requests.request("POST", url, headers=headers, data=payload)
response = r.json()
print(response)
assert r.status_code == 200
