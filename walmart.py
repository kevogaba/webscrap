import datetime
import csv
import requests 
from bs4 import BeautifulSoup

# Add additional properties, not to be prompted to "I am not Robot"
headers = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.87 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    "Accept-Encoding":"gzip, deflate",
    "DNT":"1",
    "Connection":"close", 
    "Upgrade-Insecure-Requests":"1"
    }
#Store a list of queries
items = [ 'heineken', 'Budweiser']
base_url = 'https://www.walmart.com/search?q='

#List to store scrapped products
beers = []

# Iterate inside the list of queries
for item in items:
    url = base_url + item

    html = requests.get(url, headers=headers)
    soup = BeautifulSoup(html.content, 'html5lib')
   
    # Fetch and iterate inside the container of the products to get eacg product
    all_items = soup.find('div', attrs={'class':'flex flex-wrap w-100 flex-grow-0 flex-shrink-0 ph2 pr0-xl pl4-xl mt0-xl mt3'})
    # print(all_items)
    for new in all_items:
        '''
        Block to Catch 'NoneType' exception, incase one of the properties isn't available
        Fetch the properties of each product by calling their unique properties
        '''
        try:
            # Catch NoneType error on products out of Stock
            try:
                price = new.find('div', attrs={'class':'b black f5 mr1 mr2-xl lh-copy f4-l'}).text
            except AttributeError:
                price = new.find('div', attrs={'class':'normal gray f5 mr1 mr2-xl lh-copy f4-l'}).text

            unit_price= new.find('div', attrs={'class':'f7 f6-l gray mr1'}).text
            
            product = new.find('span', attrs={'class': 'w_c'}).text

            # This property is option hence additional loop, and convert to specified output
            stock_out =  new.find('div', attrs={'class': 'sans-serif gray f7 f6-l pb2 mt3'})
            if stock_out:
                stock_out = True
            else:
                stock_out = False

        except AttributeError:
            None

        '''
        Create a dictionary to store each individual item with its specified properties
        Add the individual items into the created List
        '''
        beer = {}
        beer['scrape_date'] =datetime.datetime.now().strftime('%Y-%m-%d')
        beer['website'] = 'Walmart'
        beer['url'] = url
        beer['price'] = price
        beer['product'] = product
        beer['unit_price'] = unit_price
        beer['stock_out'] = stock_out
        beers.append(beer)

'''
save the list of items into the csv file
'''
filename = 'walmart.csv'
with open(filename, 'w', newline='') as f:
    w = csv.DictWriter(f, ['scrape_date', 'website', 'url', 
    'product', 'unit_price', 'price', 'stock_out'])
    w.writeheader()
    for beer in beers:
        w.writerow(beer)


    