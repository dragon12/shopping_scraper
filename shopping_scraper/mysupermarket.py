# -*- coding: utf-8 -*-
import requests
import re
import bs4


root_url = 'http://www.mysupermarket.co.uk/shelves/Bread_in_ASDA.html'


def contains_or_is(elem, search):
    if (isinstance(elem, list)):
        return search in elem
    else:
        return elem == search


def is_product_listing(tag):
    print "tag has class", tag['class']
    return tag.has_attr('class') and contains_or_is(tag['class'], "MspProductListCell")


def get_price_from_string(s):
    if re.match(u'£', s) is not None:
        price = re.split('\s+', s)[0]
        price = price.strip(u'£')
        return float(price)
    else:
        price = re.split('\s+', s)[0]
        price = float(price.split('\s+')[0].strip('p')) / 100
        return price


def get_product_data(tag):
    product_data = {}
    productName = tag.find("span", "ProductName").text
    nameSuffix = tag.find("span", "NameSuffix").text
    product_data['name'] = productName + nameSuffix
    product_data['price'] = get_price_from_string(tag.find("span", "Price").text)
    return product_data


def get_next_page(all):
    lookup = all.find('a', id='NextPage')
    if (not lookup):
        return None

    if (contains_or_is(lookup.get('class'), "Disabled")):
        return None

    if (lookup.has_attr('href')):
        return lookup['href']
    return None

products = []
current_url = root_url
done = False
while (not done):
    print "Querying from %s" % (current_url)
    response = requests.get(current_url)
    soup = bs4.BeautifulSoup(response.text, from_encoding='utf-8')

    productList = soup.find(id='ProductListContainer')
    listContainer = productList.ul
    listItems = listContainer.find_all('li')
    products += map(get_product_data, listContainer.find_all("div", "CellBottom"))

    current_url = get_next_page(soup)
    if (not current_url):
        done = True


print "found", len(products), "products"

for prod in products:
    print "prod: ", prod


# firstItem = listContainer.find_all("div", "CellBottom")[0]
# firstItem.find("span", "ProductName").text
# firstItem.find("span", "Price")
