import requests
from bs4 import BeautifulSoup
import lxml
from fake_useragent import UserAgent
import pandas as pd


def get_html(url):
    r = requests.get(url, headers={'User-Agent': UserAgent().chrome})
    return r.text


def get_links_dict(html):
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find('table', class_ = 'simple-little-table little trades-table').find_all('tr')
    data_links = {}
    for i in table:
        try:
            name = i.find_all('a')[0].text
            key = "{}{}".format(name,'.csv')
        except:
            name = ''
            
    links = i.find_all('a', class_ ='charticon2')
    for i in links:
        try:
            link = i.get('href')
            value = '{}{}{}'.format('https://smart-lab.ru', link, 'MSFO/download/')
        except:
            link = ''
        data = {key:value}
        data_links.update(data)
    return data_links


def get_file(links):
    for key, value in links.items():
        FILENAME = key
        NEWNAME = '{}{}'.format(key.split('.')[0],'-годовой-отчёт.csv')
        try:
            f = open(FILENAME,"wb")
            ufr = requests.get(value)
            f.write(ufr.content)
            f.close()

            df = pd.read_csv(FILENAME, delimiter=';')[['Unnamed: 0', '2016', '2017', '2018', '2019', 'LTM']]
            df.to_csv(NEWNAME, index=False)

            print('file {} is written'.format(NEWNAME))
        except:
            print('file {} not found'.format(NEWNAME))


def main():
    url = 'https://smart-lab.ru/q/shares_fundamental/'
    get_file(get_links_dict(get_html(url)))


if __name__ == '__main__':
    main()