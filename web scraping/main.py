
import requests
from bs4 import BeautifulSoup

for i in range(1, 51):
    url = f"https://books.toscrape.com/catalogue/category/books_1/page-{i}.html"
    response = requests.get(url)
    response = response.content
    soup = BeautifulSoup(response, 'html.parser')
    ol = soup.find('ol')

    articles = ol.find_all('article', class_='product_pod')
    for article in articles:
        image = article.find('img')
        title = image.attrs['alt']
        star = article.find('p')
        star = star['class'][1]
        price = article.find('p', class_='price_color').text
        price = float(price[1:])
        
        print(f'Title: {title}')
        print(f'Star Rating: {star}')
        print(f'Price: {price}')
        print(f'image: {image}\n')




