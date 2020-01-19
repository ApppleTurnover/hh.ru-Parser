import requests
import time
import json
from bs4 import BeautifulSoup as bs
from data.data import Data # Просто класс, в котором хранятся все данные, лул


def parse(base_url: str, headers: dict):
    session =  requests.Session()
    request = session.get(base_url, headers=headers)
    if request.status_code == 200:
        jobs = []
        soup = bs(request.content, 'lxml')
        divs = soup.find_all('div', attrs={'data-qa': "vacancy-serp__vacancy"})
        for div in divs:
            title = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'}).text
            href = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-title'})['href']
            company = div.find('a', attrs={'data-qa': 'vacancy-serp__vacancy-employer'}).text
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
        return jobs
        # print(finish-start, '\n\n')
        # print(jobs[0]['responsibility'])
    else:
        print('ERROR REQUEST' + base_url)


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
    with open('data/jobs.json', 'w', encoding='utf8') as file:
        json.dump(jobs, file, ensure_ascii=False, indent=2)




if __name__ == '__main__':
    region = Data.regions['novosibirsk']
    max = find_max_pages(Data.headers, Data.base_url(region))
    print(max)
    jobs = []
    for url in Data.pages(region, max):
        jobs.append(parse(url, Data.headers))
    save_data(list(filter(None,jobs)))
