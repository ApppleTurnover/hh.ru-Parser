from data.headers import Headers # Ну шо бы мои данные не палили, там accept и user-agent

class Data:
    headers = Headers.getheaders() # Ну сюда я их и засовываю в виде словаря

    def base_url(city:int):
        return f"https://hh.ru/search/vacancy?area={city}&text=python&page=0"

    def pages(city: int, count_pages: int):
        page = 0
        for page in range(count_pages):
            yield f"https://hh.ru/search/vacancy?area={city}&text=python&page={page}"
            page += 1


    regions = {
    'moscow': 1,
    'spb': 2,
    'novosibirsk': 4,
    'russia': 113,
    }
