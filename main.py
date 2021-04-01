import feedparser
import pyowm
from pyowm.exceptions import api_response_error, api_call_error
from telebot import types
import telebot
import COVID19Py

bot = telebot.TeleBot("1644586994:AAGtW78FVpmDscoiV-ZRWAXNvFLrJ-aKjbo")  # апи бота

owm = pyowm.OWM('797385fc66158e63cb61ac82a7d4ee8c', language="ru")  # ключ и язык


# Новости
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


# Погода
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


covid19 = COVID19Py.COVID19()


# Информация о ковид
@bot.message_handler(commands=['covid'])
def cov(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)  # быстрые кнопки
    btn1 = types.KeyboardButton('Во всём мире')
    btn2 = types.KeyboardButton('Украина')
    btn3 = types.KeyboardButton('Россия')
    btn4 = types.KeyboardButton('Беларусь')
    markup.add(btn1, btn2, btn3, btn4)

    send_message = f"<b>Привет {message.from_user.first_name}!</b>\nЧтобы узнать данные про коронавируса напишите " \
                   f"название страны, например: США, Украина, Россия и так далее\n"
    bot.send_message(message.chat.id, send_message, parse_mode='html', reply_markup=markup)

    final_message = "мир"
    get_message_bot = message.text.strip().lower()  # делаю только нижние регистры
    if get_message_bot == "сша":
        location = covid19.getLocationByCountryCode("US")
    elif get_message_bot == "украина":
        location = covid19.getLocationByCountryCode("UA")
    elif get_message_bot == "россия":
        location = covid19.getLocationByCountryCode("RU")
    elif get_message_bot == "беларусь":
        location = covid19.getLocationByCountryCode("BY")
    elif get_message_bot == "казакхстан":
        location = covid19.getLocationByCountryCode("KZ")
    elif get_message_bot == "италия":
        location = covid19.getLocationByCountryCode("IT")
    elif get_message_bot == "франция":
        location = covid19.getLocationByCountryCode("FR")
    elif get_message_bot == "германия":
        location = covid19.getLocationByCountryCode("DE")
    elif get_message_bot == "япония":
        location = covid19.getLocationByCountryCode("JP")
    else:
        location = covid19.getLatest()
        final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"

    if final_message == "мир":
        date = location[0]['last_updated'].split("T")
        time = date[1].split(".")
        final_message = f"<u>Данные по стране:</u>\nНаселение: {location[0]['country_population']:,}\n" \
                        f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n<b>" \
                        f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
                        f"{location[0]['latest']['deaths']:,}"

    bot.send_message(message.chat.id, final_message, parse_mode='html')


# @bot.message_handler(content_types=['text'])
# def lol(message):
#     final_message = ""
#     get_message_bot = message.text.strip().lower()  # делаю только нижние регистры
#     if get_message_bot == "сша":
#         location = covid19.getLocationByCountryCode("US")
#     elif get_message_bot == "украина":
#         location = covid19.getLocationByCountryCode("UA")
#     elif get_message_bot == "россия":
#         location = covid19.getLocationByCountryCode("RU")
#     elif get_message_bot == "беларусь":
#         location = covid19.getLocationByCountryCode("BY")
#     elif get_message_bot == "казакхстан":
#         location = covid19.getLocationByCountryCode("KZ")
#     elif get_message_bot == "италия":
#         location = covid19.getLocationByCountryCode("IT")
#     elif get_message_bot == "франция":
#         location = covid19.getLocationByCountryCode("FR")
#     elif get_message_bot == "германия":
#         location = covid19.getLocationByCountryCode("DE")
#     elif get_message_bot == "япония":
#         location = covid19.getLocationByCountryCode("JP")
#     else:
#         location = covid19.getLatest()
#         final_message = f"<u>Данные по всему миру:</u>\n<b>Заболевших: </b>{location['confirmed']:,}\n<b>Сметрей: </b>{location['deaths']:,}"
#
#     if final_message == "":
#         date = location[0]['last_updated'].split("T")
#         time = date[1].split(".")
#         final_message = f"<u>Данные по стране:</u>\nНаселение: {location[0]['country_population']:,}\n" \
#                         f"Последнее обновление: {date[0]} {time[0]}\nПоследние данные:\n<b>" \
#                         f"Заболевших: </b>{location[0]['latest']['confirmed']:,}\n<b>Сметрей: </b>" \
#                         f"{location[0]['latest']['deaths']:,}"
#
#     bot.send_message(message.chat.id, final_message, parse_mode='html')


# @bot.message_handler(content_types=['text'])
# def mess(message):


bot.polling(none_stop=True)
