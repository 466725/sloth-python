import requests
from fake_useragent import UserAgent

if __name__ == "__main__":
    print("Googling.....")
    url = "https://www.google.com/search?q=python"
    print(requests.get(url, headers={"User-Agent": UserAgent().random}).text)
