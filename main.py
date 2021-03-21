import feedparser
import pyowm
from pyowm.exceptions import api_response_error, api_call_error
import telebot
from selenium import webdriver
from time import sleep

bot = telebot.TeleBot("1644586994:AAGtW78FVpmDscoiV-ZRWAXNvFLrJ-aKjbo")  # апи бота

owm = pyowm.OWM('797385fc66158e63cb61ac82a7d4ee8c', language="ru")  # ключ и язык

#driver = webdriver.Edge('C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')


#@bot.message_handler(commands=['search_in_youtube'])
#def search_youtube(message):
  #  messages = bot.send_message(message.chat.id, "Введите текст, который хотите найти на YouTube?")
  #  bot.register_next_step_handler(messages, search)  # после вызова команды search_in_youtube идет это команда


#@bot.message_handler(content_types='text')
#def text(message):
  #  pass


#def search(message):
 #   bot.send_message(message.chat.id, "Начинаю поиск")
  #  link = "https://www.youtube.com/results?search_query=" + message.text  # ссылка на поиск видео в YouTube
   # driver.get(link)
   # video = driver.find_element_by_id("video-title")  # элементы на ютую видео
   # for i in range(len(video)):
   #     bot.send_message(message.chat.id, video[i].get_attribute('href'))


@bot.message_handler(commands=['news'])
def news(message):
    def parseRSS(rss_url):
        return feedparser.parse(rss_url)

    def getHeadlines(rss_url):
        headlines = []

        feed = parseRSS(rss_url)
        for newsitem in feed['items']:
            # headlines.append(newsitem['title'])
            headlines.append(newsitem['link'])
            # headlines.append(newsitem['id'])
            # headlines.append(newsitem['summary'])
            # headlines.append(newsitem['published'])

        return headlines

    allheadlines = []

    newsurls = {
        'googlenews': 'https://news.google.com/rss?hl=ru&gl=RU&ceid=RU:ru',  # сайт с новостями
    }

    for key, url in newsurls.items():
        allheadlines.extend(getHeadlines(url))

    for hl in allheadlines:
        pass
        bot.send_message(message.chat.id, hl)


@bot.message_handler(commands=['weather'])
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


bot.polling(none_stop=True)
