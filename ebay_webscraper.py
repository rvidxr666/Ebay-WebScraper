from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd

driver = webdriver.Chrome('C:\Program Files (x86)\chromedriver.exe')


# Getting an Input of a person and creating a url
def get_input():
    req = input('Write your request ')
    template = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw={}&_sacat=0"
    request = req.replace(' ', '+')
    url = template.format(request)
    driver.get(url)
    return BeautifulSoup(driver.page_source, 'lxml')


#Searching for ads and adding them into the Dataframe
def title_and_price(parsed_page_src):
    a ={}
    urls = {}
    k = 0
    while k != 61:
        k += 1
        try:
            ad = parsed_page_src.find('li', {'data-view':'mi:1686|iid:{}'.format(k)})
            text = ad.find('h3').text
            if 'New Listing' in text:
                text = text.replace('New Listing', '')
            price = ad.find('span', {'class':'s-item__price'}).text
            a[text] = price
            urls[ad.find('a', {'class': 's-item__link'})['href']] = price
            if len(urls) == 20:
                break

        except:
            break

    dict_for_df = {'Ads': list(a.keys()), 'Price': list(a.values())}
    df = pd.DataFrame(data=dict_for_df)
    return df


def sort_ads(dataframe, assc):
    float_list = []
    for cost in list(dataframe['Price']):
        if 'to' in cost:
            ind = cost.find('to')
            elm1 = float(cost[:ind-1].replace('$', ''))
            elm2 = float(cost[ind+2:].replace('$', ''))
            float_list.append((elm1+elm2)/2)
        else:
            float_list.append(float(cost.replace('$', '').replace(',', '')))

    dataframe['float_price'] = float_list
    dataframe.sort_values(by = 'float_price', inplace=True, ascending = assc)
    del dataframe['float_price']
    return dataframe


def enter_the_next_page():
    next_page = driver.find_element_by_class_name('pagination__next').get_attribute('href')
    driver.get(next_page)
    next_page_url_parsed = BeautifulSoup(driver.page_source, 'lxml')
    return title_and_price(next_page_url_parsed)


def find_max(dataframe):
    float_price = []
    for price in dataframe['Price']:
        if 'to' in price:
            ind = price.find('to')
            elm1 = float(price[:ind-1].replace('$', ''))
            elm2 = float(price[ind+2:].replace('$', ''))
            float_price.append((elm1+elm2)/2)
        else:
            float_price.append(float(price.replace('$', '').replace(',', '')))
    dataframe['float_price'] = float_price
    max_val = dataframe[dataframe['float_price'] == max(dataframe['float_price'])]
    del max_val['float_price']
    return max_val


def find_min(dataframe):
    float_price = []
    for price in dataframe['Price']:
        if 'to' in price:
            ind = price.find('to')
            elm1 = float(price[:ind-1].replace('$', ''))
            elm2 = float(price[ind+2:].replace('$', ''))
            float_price.append((elm1+elm2)/2)
        else:
            float_price.append(float(price.replace('$', '').replace(',', '')))
    dataframe['float_price'] = float_price
    min_val = dataframe[dataframe['float_price'] == min(dataframe['float_price'])]
    del min_val['float_price']
    return min_val


while True:
    first_user_input = input('You want to continue/start? Press Yes/No ')

    user_request = get_input()
    user_df = title_and_price(user_request)
    print(user_df)
    while True:
        user_input = input('Write - "Sort", to sort the DF; Write - "Min" or "Max" to find the cheapest/most expensive ads;' +
                           ' Write "Next" to enter the next page; Write "Another" to make another request ')
        user_input = user_input.strip().lower()
        if user_input == 'sort':
            print(sort_ads(user_df, False))
        if user_input == 'max':
            print(find_max(user_df))
        if user_input == 'min':
            print(find_min(user_df))
        if user_input == 'next':
            user_df = enter_the_next_page()
            print(user_df)
        if user_input == 'another':
            break




















