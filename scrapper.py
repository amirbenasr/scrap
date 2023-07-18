import requests
from bs4 import BeautifulSoup
import csv
import re

# Function to scrape book titles from a page
x = 1


class Person:
    def __init__(self, name, lname, state, city, phone, email):
        self.name = name
        self.lname = lname
        self.state = state
        self.phone = phone
        self.email = email
        self.city = city


list = []


def scrape_page(url):
    print("scrapping"+url)
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'lxml')
    rows = soup.find_all(
        'tr', id=re.compile("^info"))

    print(len(rows))
    for idx, row in enumerate(rows):
        childrens = row.findAll('ul', class_="list")
        for i, child in enumerate(childrens):
            if (i == 0):
                spans = child.findAll('span')
                name = spans[0].text.strip()
                lname = spans[1].text.strip()
                print(name, lname)

            elif (i == 1):
                spans = child.findAll('span')
                state = spans[0].text.strip()
                city = spans[1].text.strip()
                print(state, city)

            elif (i == 2):
                spans = child.findAll('span')
                phone = spans[0].text.strip()
                email = spans[3].text.strip()
                print(phone, email)
        list.append(Person(name, lname, state, city, phone, email))


def write_list_tocsv(list):

    row_list = [["Name", "Last Name", "State", "City", "Phone", "Email"]]

    for person in list:
        row_list.append([person.name, person.lname,
                        person.state, person.city, person.phone, person.email])

    with open('advocats.csv', 'w', newline='') as file:
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
initial_url = 'https://avocat.org.tn/annuaire_des_avocats_--0-0-1----'

while (x <= 199):
    scrape_page(initial_url+str(x))
    x += 1
    # navigate_next(initial_url)

write_list_tocsv(list)
