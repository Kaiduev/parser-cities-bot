import requests
from bs4 import BeautifulSoup as bs


def parse_cities():
    url = "https://ru.wikipedia.org/wiki/Городские_населённые_пункты_Московской_области"
    page = requests.get(url)
    soup = bs(page.text, "html.parser")
    table = soup.find_all('table', class_="standard sortable")[0]
    tbody = table.find('tbody')
    list_of_tr = tbody.find_all('tr')
    list_of_tr.pop(1)
    cities = list()
    for tr in list_of_tr:
        list_of_td = tr.find_all('td')
        temp_variable = dict()
        for td in list_of_td:
            if list_of_td.index(td) == 1 or list_of_td.index(td) == 2 or list_of_td.index(td) == 4:
                if list_of_td.index(td) == 1:
                    a_tag = td.find('a', href=True)
                    temp_variable["name"] = a_tag["title"]
                    temp_variable["url"] = "https://ru.wikipedia.org/{}".format(a_tag["href"])
                if list_of_td.index(td) == 2:
                    a_tag = td.find('a', href=True)
                    temp_variable["name2"] = a_tag.text
                if list_of_td.index(td) == 4:
                    temp_variable["people_quantity"] = td["data-sort-value"]
        cities.append(temp_variable)
    return cities

