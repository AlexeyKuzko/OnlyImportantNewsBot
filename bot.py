import telebot

TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def welcome(message):
    bot.reply_to(message, """\
Hi there, I am OnlyImportantNewsBot.
At this moment I can only echo messages. What do you want me to echo?\
""")


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, message.text)


bot.infinity_polling()
