import requests
import os
import time
import json

from bs4 import BeautifulSoup as bs
from data.data import Data

path = os.path.join(os.path.dirname(__file__))
print(path)


def parse(headers: dict, pages:'generator'):
    session = requests.Session()
    jobs = []
    for url in pages:
        count = 1
        while count != 0 and count < 3:
            request = session.get(url, headers=headers)
            if request.status_code == 200:
                soup = bs(request.content, 'lxml')
                divs = soup.find_all('div', attrs={'data-qa': "vacancy-serp__vacancy"})
                for div in divs:
                    title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
                    href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
                    try:
                        company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
                    except(AttributeError):
                        company = 'Не указано'
                    responsibility = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).text
                    requirement = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy_snippet_requirement'}).text
                    try:
                        salary = div.find('div', attrs={'data-qa': 'vacancy-serp__vacancy-compensation'}).text
                    except(AttributeError):
                        salary = 'Не указано'
                    jobs.append({
                        'title': title,
                        'company': company,
                        'salary': salary,
                        'href': href,
                        'responsibility': responsibility,
                        'requirement': requirement,
                    })
                break
            else:
                count += 1
                print('Oops..')
                session = requests.Session()
        else:
            print('ERROR REQUEST' + url)
    return jobs
    # print(finish-start, '\n\n')
    # print(jobs[0]['responsibility'])


def find_max_pages(headers: dict, base_url: str):
    session = requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        time.sleep(1)
        last_page = 0
        soup = bs(request.content, 'lxml')
        last_page = int(soup.find_all('a', attrs={'data-qa': 'pager-page'})[-1].text)
        return last_page
    else:
        raise('ERROR REQUEST')


def save_data(jobs):
    with open(f'{path}/data/jobs.json', 'w', encoding='utf8') as file:
            json.dump(jobs, file, ensure_ascii=False, indent=2)




if __name__ == '__main__':
    region = Data.regions['novosibirsk']
    max = find_max_pages(Data.headers, Data.base_url(region))
    print(max)
    jobs = list(parse(Data.headers, Data.pages(region, max)))
    save_data(list(filter(None,jobs)))
