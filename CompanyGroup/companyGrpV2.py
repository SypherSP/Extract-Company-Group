from bs4 import BeautifulSoup
import requests
import xlsxwriter

list_of_companies = []
companies_info = {}
html_text = ""
not_found_msg = 'Unavailable'


def takeInput():
    global html_text

    print("Enter the URL of the zaubacorp search result (https://www.zaubacorp.com/) : ")
    URL = input('>').strip()
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
            pair = (tag.text, tag['href'])
            list_of_companies.append(pair)

    list_of_companies = set(list_of_companies)


def getInfo():
    for name, URL in list_of_companies:
        infoHelper(name,URL)
        # html = requests.get(URL).text
        # soup = BeautifulSoup(html, 'lxml')
        # companies_info[name] = {}
        # try:
        #     companies_info[name]['url'] = URL
        #     companies_info[name]['roc'] = soup.find(
        #         'p', text='RoC').parent.find_next('td').p.text[4:]
        #     companies_info[name]['status'] = soup.find(
        #         'p', text='Company Status').parent.find_next('td').p.span.text
        #     date = soup.find(
        #         'p', text='Date of Incorporation').parent.find_next('td').p.text
        #     companies_info[name]['date_of_incorporation'] = date[0:6]+date[-5:]
        #     try:
        #         companies_info[name]['activity'] = soup.find(
        #             'p', text='Activity').parent.find_next('td').p.text
        #     except:
        #         companies_info[name]['activity'] = not_found_msg

        #     try:
        #         companies_info[name]['paid_up_capital'] = soup.find(
        #             'p', text='Paid up capital').parent.find_next('td').p.text
        #     except:
        #         companies_info[name]['paid_up_capital'] = not_found_msg

        #     est_dets = [td.p.text for td in soup.find(
        #         'strong', text='Establishment Name').parent.parent.find_next('tr').find_all('td')]
        #     address = ''
        #     if(est_dets[0] == 'No establishments found'):
        #         address = not_found_msg
        #     else:
        #         address = f'{est_dets[0]},\n{est_dets[3]}\n{est_dets[1]}-{est_dets[2]}'
        #     companies_info[name]['establishment_details'] = address
        # except:
        #     print("Something went wrong")
        #     print(URL)
        #     del companies_info[name]


def infoHelper(name, URL):
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'lxml')
    companies_info[name] = {}
    try:
        companies_info[name]['url'] = URL
        companies_info[name]['roc'] = soup.find(
            'p', text='RoC').parent.find_next('td').p.text[4:]
        companies_info[name]['status'] = soup.find(
            'p', text='Company Status').parent.find_next('td').p.span.text
        date = soup.find(
            'p', text='Date of Incorporation').parent.find_next('td').p.text
        companies_info[name]['date_of_incorporation'] = date[0:6]+date[-5:]
        try:
            companies_info[name]['activity'] = soup.find(
                'p', text='Activity').parent.find_next('td').p.text
        except:
            companies_info[name]['activity'] = not_found_msg

        try:
            companies_info[name]['paid_up_capital'] = soup.find(
                'p', text='Paid up capital').parent.find_next('td').p.text
        except:
            companies_info[name]['paid_up_capital'] = not_found_msg

        est_dets = [td.p.text for td in soup.find(
            'strong', text='Establishment Name').parent.parent.find_next('tr').find_all('td')]
        address = ''
        if(est_dets[0] == 'No establishments found'):
            address = not_found_msg
        else:
            address = f'{est_dets[0]},\n{est_dets[3]}\n{est_dets[1]}-{est_dets[2]}'
        companies_info[name]['establishment_details'] = address
    except:
        print("Something went wrong")
        print(URL)
        del companies_info[name]

def info1company():
    URL = "https://www.zaubacorp.com/company/DABUR-FOODS-LIMITED/U15202DL1996PLC083594"
    html = requests.get(URL).text
    soup = BeautifulSoup(html, 'lxml')

    info = {}
    info['url'] = URL

    tab = soup.table
    info['roc'] = tab.find(
        'p', text='RoC').parent.find_next('td').p.text[4:]
    info['status'] = tab.find(
        'p', text='Company Status').parent.find_next('td').p.span.text
    date = tab.find(
        'p', text='Date of Incorporation').parent.find_next('td').p.text
    info['date_of_incorporation'] = date[0:6]+date[-5:]

    try:
        info['activity'] = tab.find(
            'p', text='Activity').parent.find_next('td').p.text
    except:
        info['activity'] = not_found_msg

    try:
        info['paid_up_capital'] = soup.find(
            'p', text='Paid up capital').parent.find_next('td').p.text
    except:
        info['paid_up_capital'] = not_found_msg

    est_dets = [td.p.text for td in soup.find(
        'strong', text='Establishment Name').parent.parent.find_next('tr').find_all('td')]
    address = ''
    if(est_dets[0] == 'No establishments found'):
        address = not_found_msg
    else:
        address = f'{est_dets[0]},\n{est_dets[3]}\n{est_dets[1]}-{est_dets[2]}'
    info['establishment_details'] = address

    # for key, value in info.items():
    #     print(key, value)


def writeToFile():
    workbook = xlsxwriter.Workbook('Information_on_company_group.xlsx')

    sheet = workbook.add_worksheet()
    sheet.write(0, 0, "Name")
    sheet.write(0, 1, "RoC")
    sheet.write(0, 2, "Est Details")
    sheet.write(0, 3, "Inc Date")
    sheet.write(0, 4, "Status")
    sheet.write(0, 5, "Activity")
    sheet.write(0, 6, "Paid up capital")
    row = 1
    for name, info in companies_info.items():
        sheet.write(row, 0, name)
        sheet.write(row, 1, info['roc'])
        sheet.write(row, 2, info['establishment_details'])
        sheet.write(row, 3, info['date_of_incorporation'])
        sheet.write(row, 4, info['status'])
        sheet.write(row, 5, info['activity'])
        sheet.write(row, 6, info['paid_up_capital'])
        row += 1
    workbook.close()


def main():
    # info1company()

    takeInput()
    getList()
    getInfo()
    writeToFile()

    print("\nList of companies can be viewed in \'Information_on_company_group.xlsx\' file\nTASK COMPLETED")
    input("\nPress enter to exit...")


if __name__ == "__main__":
    main()
