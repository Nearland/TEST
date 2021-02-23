import pyowm
import telebot

bot = telebot.TeleBot("1644586994:AAGtW78FVpmDscoiV-ZRWAXNvFLrJ-aKjbo")  # апи бота

owm = pyowm.OWM('797385fc66158e63cb61ac82a7d4ee8c', language="ru")  # ключ и язык


@bot.message_handler(content_types=['text'])  # отвечает на тип текст
def send_echo(message):  # дублирует
    #bot.reply_to(message, message.text)
    observation = owm.weather_at_place(message.text)  # Место где будет показывавть погоду
    w = observation.get_weather()
    temp = w.get_temperature('celsius')["temp"]  # получение температуры
    wind = w.get_wind()["speed"]  # Скрость ветра
    tomorrow = pyowm.timeutils.tomorrow()  # погода на завтра

    answer = "В городе/стране " + message.text + " сейчас " + w.get_detailed_status() + "\n"
    answer += "Сейчас примерно " + str(temp) + " °C" + "\n"
    answer += "Ветер " + str(wind) + " м/c" + "\n"
    bot.send_message(message.chat.id, answer)


bot.polling(none_stop=True)
