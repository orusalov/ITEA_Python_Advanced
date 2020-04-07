import requests as r
from bs4 import BeautifulSoup

class Err404(Exception):
    pass


class Weather:
    URL = 'https://sinoptik.ua'
    DAYS = {
        0: 'сегодня',
        1: 'завтра',
        2: 'послезавтра',
        3: '3 дня вперед',
        4: '4 дня вперед',
        5: '5 дней вперед',
        6: '6 дней вперед',
        7: '7 дней вперед',
        8: '8 дней вперед',
        9: '9 дней вперед'
    }

    def __init__(self, city=None):
        self.city = city
        self.url = f'{self.URL}{f"/погода-{city}" if city else ""}/10-дней'
        self.weather = self.get_weather(self.url)

    def get_weather(self, url):
        page = r.get(url)

        if page.status_code == 404:
            raise Err404('город не найден')

        soup = BeautifulSoup(page.content, 'html.parser')

        return_ = {}
        weather_by_day = {}
        return_['city'] = soup.find('div', class_="cityName cityNameShort").find('h1').get_text().strip()
        for index, day_soup in enumerate(soup.find_all('div', class_='main')):
            wd = {}
            date = f"{day_soup.find(class_='day-link').get_text()}, \
{day_soup.find(class_='date').get_text()} {day_soup.find(class_='month').get_text()}"
            sky = day_soup.find_all('div', class_='weatherIco')[0]['title']
            temperature = day_soup.find(class_='temperature').get_text().strip()
            wd["date"] = date
            wd["sky"] = sky
            wd["temperature"] = temperature
            weather_by_day[index] = wd

        return_['forecast'] = weather_by_day
        return return_

    def print_weather_for_N_day(self, day=0):
        print(f'{self.weather["city"]} на {self.DAYS[day]}:')
        wd = self.weather['forecast'][day]
        print(wd['date'], wd['sky'], wd['temperature'], sep=', ')

if __name__ == '__main__':
    weather = Weather()

    print('(по умолчанию)')
    default = True
    while True:
        if default:
            weather.print_weather_for_N_day()
            default = False

        try:
            choice = input('Выберите другой день(0-9)* или город(г)\n*0-9: 0 - сегодня, 1 - завтра и т.д\n').lower().strip()
            if len(choice) == 1 and ('0' <= choice <= '9'):
                weather.print_weather_for_N_day(int(choice))
            elif choice == 'г':
                city = input('Напишите название города: ').lower().strip()
                prev_weather = weather
                weather = Weather(city=city)
                del prev_weather
                default = True
            else:
                print('Неправильный ввод, до свидания')
                break
        except Err404 as err:
            print(err)
            weather = prev_weather
