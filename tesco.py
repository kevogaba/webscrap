import datetime
import re
import csv
from tokenize import group
import requests 
from bs4 import BeautifulSoup

headers = {'User-Agent': 'Chrome/96.0.4664.45'}
items = ['heineken', 'Budweiser', 'Calsberg']
base_url = "https://www.tesco.com/groceries/en-GB/search?query="

beers = []

for item in items:
    url = base_url + item
    # Url.append(url)

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'html5lib')
   
    all_items = soup.find('ul', attrs={'class':'product-list grid'})
    '''
    Fetch the properties of each product by calling their unique properties
    Fetch and iterate inside the container of the products to get eacg product
    '''
    for new in all_items:
        price = new.find('div', attrs={'class':'price-control-wrapper'}).text

        unit_price= new.find('div', attrs={'class':'price-per-quantity-weight'}).text

        detail = new.find('div', attrs={'class':'list-item-content promo-content-small'})
        if detail:
            promo = detail.span.text
        else:
            promo = None

        product_quantity = new.find('h3').text

        y = re.split(r'\W+', product_quantity)

        for i in y: 
            match = re.search(r'(\d+)(Ml)', i)
            new = re.search(r'(X)(\d+)', i)
            if new:
                product = ' '.join(y[0:-1])
                quantity = i
            else:
                if match:
                    product = ' '.join(y[0:(len(y)-1)])
                    quantity = y[-1]

                if i == 'X':
                    x = (y.index(i))
                    quantity = ' '.join(y[(x-1):(x+2)])
                    product = ' '.join(y[0:(x-2)])
                else:
                    pass

        '''
        Create a dictionary to store each individual item with its specified properties
        Add the individual items into the created List
        '''
        beer = {}
        beer['scrape_date'] =datetime.datetime.now().strftime('%Y-%m-%d')
        beer['website'] = 'Tesco'
        beer['url'] = url
        beer['product'] = product_quantity
        beer['quantity'] = quantity
        beer['unit_price'] = unit_price
        beer['price'] = price
        beer['promo'] = promo
        beers.append(beer)

    
'''
save the list of items into the csv file
'''
filename = 'tesco.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['scrape_date', 'website', 'url', 
    'product', 'quantity', 'unit_price', 'price', 'promo'])
    w.writeheader()
    for beer in beers:
        w.writerow(beer)

    