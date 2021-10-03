
from os import write
from bs4 import BeautifulSoup
import requests

list_of_companies = []
html_text = ""


def takeInput():
    global html_text
    print("Enter the URL of the saubacorp search result: ")
    URL = input('>')
    html_text = requests.get(URL).text


def getList():
    global list_of_companies

    soup = BeautifulSoup(html_text, 'lxml')
    hidden_rows = soup.find_all('td', class_='hiddenRow')
    a_tags = []
    for row in hidden_rows:
        a_tags.extend(row.find_all('a'))
    for tag in a_tags:
        if tag.text != 'Login':
            list_of_companies.append(tag.text)
    list_of_companies = set(list_of_companies)


def writeToFile():
    with open("group_companies.txt", 'w') as file:
        for company in list_of_companies:
            file.write(f"{company}\n")


def main():
    takeInput()
    getList()
    writeToFile()
    print("List of companies can be viewed in \'group_companies.txt\' file\nTASK COMPLETED")
    input("Press enter to exit...")


if __name__ == "__main__":
    main()
