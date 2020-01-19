from data.headers import Headers # Ну шо бы мои данные не палили, там accept и user-agent

class Data:
    headers = Headers.getheaders() # Ну сюда я их и засовываю в виде словаря

    def base_url(city:int):
        return f"https://hh.ru/search/vacancy?area={city}&text=python&page=0"

    citys = {
    'moscow': 1,
    'spb': 2,
    'novosibirsk': 4,
    }
