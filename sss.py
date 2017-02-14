import threading
import time

import requests

from bs4 import BeautifulSoup


BASE_URL = 'http://brickset.com/sets/year-2016'

def get_url():
    ss = requests.get(BASE_URL)
    base_soup = BeautifulSoup(ss.content, 'lxml')
    page_url_list = {page.find_next('a').get('href') for page in base_soup.find_all('li', class_='page')}
    #page_url_list = list(page_url_list).append(BASE_URL)
    #print(page_url_list)
    return page_url_list

def download_image(page_url):
    page_content = requests.get(page_url).content
    page_soup = BeautifulSoup(page_content, 'lxml')
    image_list = [image_url.get('src') for image_url in page_soup.find_all('img')]
    
    for image in image_list:
        try:
            with open(image.split('?')[-1]+'.jpg', 'wb') as f:
                f.write((requests.get(image)).content)
        except FileNotFoundError:
            pass
print(get_url())

def start_thread():
    for page_url in get_url():
        print(page_url)
        #download_image(page_url)
        threading.Thread(target=download_image, args=(page_url,)).start()


if __name__ == '__main__':
    start = time.time()
    start_thread()
    time_need = time.time() - start
    print(time_need)
