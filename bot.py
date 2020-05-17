import config
import telebot
import utils
from telebot import types

lib = dict()

url = {'Ужасы':'https://knigopoisk.org/ratings/luchshie_knigi_uzhasov',
       'Антиутопия':'https://knigopoisk.org/ratings/knigi_antiutopiya',
       'Реализм':'https://knigopoisk.org/ratings/knigi_realizm',
       'Фантастика':'https://knigopoisk.org/ratings/knigi_fantastika_luchshee',
       'Детективы':'https://knigopoisk.org/ratings/knigi_detektivy',
       'Детские':'https://knigopoisk.org/ratings/knigi_skazki',
       'Новеллы':'https://knigopoisk.org/ratings/knigi_novella',
       'Исторические романы':'https://knigopoisk.org/ratings/knigi_istoricheskie_romany' }

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands = ['start'])
def Hello(message):
    bot.send_message(message.chat.id,'Здравствуйте, я ваш консультант')
    markup = types.ReplyKeyboardMarkup()
    markup.row('Топ книг по жанрам')
    markup.row('Поиск книг по автору/названию')
    bot.send_message(message.chat.id,'Выберите нужный вам вариант: ', reply_markup=markup)

@bot.message_handler(regexp='Топ книг по жанрам')
def Buttons(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('назад')
    markup.row('Ужасы')
    markup.row('Антиутопия')
    markup.row('Реализм')
    markup.row('Фантастика')
    markup.row('Детективы')
    markup.row('Детские')
    markup.row('Новеллы')
    markup.row('Исторические')
    bot.send_message(message.chat.id, "Выберите жанр:", reply_markup=markup)


@bot.message_handler(regexp='Ужасы')
def Horror(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Ужасы'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Антиутопия')
def Antiut(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Антиутопия'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Реализм')
def Real(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Реализм'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Фантастика')
def Fantasy(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Фантастика'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Детективы')
def Detect(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Детективы'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Детские')
def Fairytail(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Детские'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Новеллы')
def Novel(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Новеллы'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='Исторические')
def HistRoman(message):
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton("Показать", callback_data=str(message.chat.id) + ' ' + 'Исторические'))
    bot.send_message(message.chat.id, "Хочу посоветовать вам следующие 10 замечательных книг", reply_markup=keyboard)


@bot.message_handler(regexp='назад')
def Hello(message):
    markup = types.ReplyKeyboardMarkup()
    markup.row('Топ книг по жанрам')
    markup.row('Поиск книг по автору/названию')
    bot.send_message(message.chat.id,'Выбирайте: ', reply_markup=markup)


@bot.message_handler(regexp='Поиск')
def SearchBooksAndAuthors(message):
    bot.send_message(message.chat.id, 'Введите имя и фамилию автора или название книги:', None)
    @bot.message_handler(content_types=["text"])
    def Polling(message):
        global lib
        lib = utils.ReturnLib()
        x = max(utils.FindingOut(utils.CorrectMistakes(message.text, lib)),utils.FindingOut(utils.CorrectMistakesAuth(message.text, lib)))
        if x == 0:
            bot.send_message(message.chat.id, utils.ReturnForBook(message.text), None)
        elif x == 1:
            bot.send_message(message.chat.id, utils.ReturnForAuthor(message.text), None)
        elif x == -1:
            bot.send_message(message.chat.id, 'Ничего не найдено!', None)


@bot.callback_query_handler(func=lambda c: True)
def inline(c):
    global lib
    a = c.data.split(' ')
    f = utils.GetCode(url[a[1]])
    local_authors, local_names = utils.AuthorAndName(f)
    s = utils.MakeTop(local_authors, local_names, 10)
    bot.send_message(a[0], s, None)



if __name__ == '__main__':
    bot.polling(none_stop=True)



