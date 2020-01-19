import requests
from bs4 import BeautifulSoup as bs
from data.data import Data # Просто класс, в котором хранятся все данные, лул


def parse(base_url: str, headers: dict):
    session =  requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        soup = bs(request.content, 'html.parser')
        divs = soup.find_all('div', attrs={'data-qa': "vacancy-serp__vacancy"})
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
            print(f"{href=}\n {title=}   {company=}\n")
    else:
        print('ERROR')


if __name__ == '__main__':
    parse(Data.base_url(Data.citys['moscow']), Data.headers)
