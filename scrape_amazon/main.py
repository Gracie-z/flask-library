import requests
from bs4 import BeautifulSoup
from urllib.request import urlretrieve
from db_config import save_info, close_db
import os


headers = {
    'User-Agent': 'Mozilla/5.0 (X11; CrOS x86_64 8172.45.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.64 Safari/537.36'}
html = requests.get('https://www.amazon.com/b/ref=bhp_brws_100bks/140-5874772-1432812?ie=UTF8&node=8192263011&pf_rd_m=ATVPDKIKX0DER&pf_rd_s=merchandised-search-leftnav&pf_rd_r=XYAPXTG9SHPSP4YTWB32&pf_rd_r=XYAPXTG9SHPSP4YTWB32&pf_rd_t=101&pf_rd_p=dfe90ba6-2174-4c8c-9c55-9e9b4d012467&pf_rd_p=dfe90ba6-2174-4c8c-9c55-9e9b4d012467&pf_rd_i=283155', headers=headers)
bs = BeautifulSoup(html.content, 'html.parser')


line = bs.find('ol', {'class': 'a-carousel'})
for book in line.find_all('li', {'class': 'a-carousel-card acswidget-carousel__card'}):
    items = book.find_all('span', {'class': 'a-truncate-full'})
    book_name = items[0].text.strip()
    book_authors = items[1].text.strip()
    image = book.find('img')['src']
    urlretrieve(image,f'./images/{book_name.strip()}.jpg')
    pic_dir = os.path.join(os.getcwd()+f'./images/{book_name.strip()}.jpg')
    save_info(book_authors, book_name, pic_dir)

close_db()