from bs4 import BeautifulSoup
import json
import math
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import time


def scrape(url):
    print("Starting webdriver...")
    options = Options()
    options.headless = True
    driver = webdriver.Firefox(options=options)

    print('Requesting data from url...')
    driver.get(url)

    print('Parsing data...')
    soup = BeautifulSoup(driver.page_source, "lxml")

    reviews = soup.find('div', class_='bPhtn').find_all('div', recursive=False)

    total_reviews = int(soup.find('div', class_='cIUfa Ci').text[-4:])
    # if total reviews goes over 999 the script wont work. 
    # -5 banaidine ani (lol).

    data = []

    try:
        # run iteration for x times calculating x as ceil(max approx) of total reviews / 10
        for _ in range(math.ceil(total_reviews / 10.0)):
            for review in reviews[:-1]:
                data.append({
                    'title': review.find('div', class_='WlYyy cPsXC bLFSo cspKb dTqpp').text,
                    'date': review.find('div', class_='fEDvV').text,
                    'content': review.find('div', class_='WlYyy diXIH dDKKM').text,
                })
            print('New data: ')
            print(data)
            # overrwite data to file on every iteration in case of fail
            with open('result.json', 'w') as fp:
                json.dump(data, fp)
            # click next button for more reviews and wait 15 secs for it to load
            next_btn = driver.find_element(class_='dfuux f u j _T z _F _S ddFHE bVTsJ emPJr')
            next_btn.click()
            print('Sleeping for 15 secs for new reviews to load')
            time.sleep(15000)
    except Exception as e:
        print(e)
    
    return data

if __name__ == '__main__':
    URLS = [
        'https://www.tripadvisor.com/Attraction_Review-g1367591-d8409217-Reviews-Chitwan_National_Park-Sauraha_Chitwan_District_Narayani_Zone_Central_Region.html',
    ]

    for url in URLS:
        data = scrape(url)
        # final data^