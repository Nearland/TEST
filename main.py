import feedparser
import pyowm
from pyowm.exceptions import api_response_error, api_call_error
import telebot

bot = telebot.TeleBot("1644586994:AAGtW78FVpmDscoiV-ZRWAXNvFLrJ-aKjbo")  # апи бота

owm = pyowm.OWM('797385fc66158e63cb61ac82a7d4ee8c', language="ru")  # ключ и язык


# @bot.message_handler(content_types=['text'])  # отвечает на тип текст
def weather(message):  # дублирует
    try:
        city_name = message.text[9:]  # цифра 9 удаляет слово weather

        bot.send_message(message.chat.id, "Погода в городе " + city_name)
        observation = owm.weather_at_place(city_name)  # Место где будет показывавть погоду
        w = observation.get_weather()
        temp = w.get_temperature('celsius')["temp"]  # получение температуры
        wind = w.get_wind()["speed"]  # Скрость ветра
        answer = "В городе/стране " + city_name + " сейчас " + w.get_detailed_status() + "\n"
        answer += "Сейчас примерно " + str(temp) + " °C" + "\n"
        answer += "Ветер " + str(wind) + " м/c" + "\n"
        bot.send_message(message.chat.id, answer)  # ввывод в телеграмм
    except api_response_error.NotFoundError:
        bot.send_message(message.chat.id, "Нет данных город/страна " + city_name)
        pass
    except api_call_error.APICallError:
        if city_name == "":
            bot.send_message(message.chat.id, "Вы не ввели город/страна")
            pass


def news(message):
    def parseRSS(rss_url):
        return feedparser.parse(rss_url)

    def getHeadlines(rss_url):
        headlines = []

        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            #headlines.append(newsitem['title'])
            headlines.append(newsitem['link'])
            # headlines.append(newsitem['id'])
            # headlines.append(newsitem['summary'])
            # headlines.append(newsitem['published'])

        return headlines

    allheadlines = []

    newsurls = {
        'googlenews': 'https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru',
    }

    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))

    for hl in allheadlines:
        pass
        bot.send_message(message.chat.id, hl)


@bot.message_handler(commands=['news'])
def command2(message):
    news(message)


@bot.message_handler(commands=['weather'])
def command1(message):
    weather(message)


bot.polling(none_stop=True)
