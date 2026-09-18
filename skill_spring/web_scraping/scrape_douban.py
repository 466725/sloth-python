import requests
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Mozilla/5.0'}
for start_number in range(0, 250, 25):
    # print(start_number)
    response = requests.get("https://movie.douban.com/top250?start={}&filter=".format(start_number), headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    for item in soup.find_all('div', class_='item'):
        title = item.find('span', class_='title').text
        rating = item.find('span', class_='rating_num').text
        print(title, rating)