import telebot
from telebot import types
import requests

TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help', 'start'])
def welcome(message):
    bot.reply_to(message, """\
Hi there, I am OnlyImportantNewsBot.
Send /search [channel_name] [words] to search for specific words in a channel's messages.
Example: /search @publicchannelname important news\
""")


@bot.message_handler(commands=['search'])
def search_channel_messages(message):
    try:
        _, channel_name, *search_words = message.text.split()
        search_words = set(search_words)
    except ValueError:
        bot.reply_to(message, "Please provide the channel name and words to search for. Example: /search @publicchannelname important news")
        return

    url = f'https://api.telegram.org/bot{TOKEN}/getUpdates'
    response = requests.get(url)
    data = response.json()

    if data['ok']:
        messages = data['result']
        found_messages = []

        latest_message = None

        for msg in messages:
            if 'channel_post' in msg and msg['channel_post']['chat']['username'] == channel_name[1:]:
                channel_message = msg['channel_post']['text']
                if any(word in channel_message for word in search_words):
                    found_messages.append(channel_message)
                latest_message = channel_message  # Update the latest message from the channel

        if found_messages:
            for found_message in found_messages:
                bot.send_message(message.chat.id, found_message)
        else:
            if latest_message:
                bot.send_message(message.chat.id, "No messages found with the specified words. Here is the latest message from the channel:")
                bot.send_message(message.chat.id, latest_message)
            else:
                bot.reply_to(message, "No messages found in the channel.")
    else:
        bot.reply_to(message, "Failed to fetch updates from the channel.")


@bot.message_handler(func=lambda message: True)
def echo(message):
    bot.reply_to(message, 'I can handle only /search command!')


bot.infinity_polling()