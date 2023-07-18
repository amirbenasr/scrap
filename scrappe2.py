import requests
from bs4 import BeautifulSoup
import csv
import re

# Function to scrape book titles from a page
x = 1


class Org:
    def __init__(self, name, address, phone, email):
        self.name = name
        self.phone = phone
        self.email = email
        self.address = address


list = []


def scrape_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    rows = soup.find_all(
        'ul', re.compile("^liste"))

    print(len(rows))
    for idx, row in enumerate(rows):
        childrens = row.findAll('li')
        for i, child in enumerate(childrens):
            name = child.find('a').text.strip()
            ps = child.findAll('p')
            for i, p in enumerate(ps):
                print("ps0", p[0])
                if (i == 0):
                    address = p.text.split(':')[1].strip()
                    print(address)
                if (i == 1):
                    phone = p.text.split(':')[1].strip()
                if (i == 2):
                    print(p)
                    email = p.text.split(':')[1].strip()
                    list.append(Org(name, address, phone, email))


def write_list_tocsv(list):

    row_list = [["Name", "Adress", "Phone", "Email"]]

    for person in list:
        row_list.append([person.name, person.address,
                        person.phone, person.email])

    with open('orgs.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(row_list)


def navigate_next(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    print("----"+str(x))
    next_link = soup.find('a', href="annuaire_des_avocats_--0-0-1----10")
    print(next_link)
    if next_link:
        next_url = 'https://avocat.org.tn/'+next_link['href']
        print(next_url)
    scrape_page(next_url)


# Start scraping from the initial page
initial_url = 'http://fr.tunisie.gov.tn/11-annuaire-d-administration.htm?ip=1'

while (x <= 1):
    scrape_page(initial_url+str(x))
    x += 1
    # navigate_next(initial_url)

# print(len(list))
write_list_tocsv(list)
