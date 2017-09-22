from twx.botapi import TelegramBot, ReplyKeyboardMarkup
import os, requests, json


bot = TelegramBot(os.getenv('TELEGRAM_BOT_TOKEN'))
updates = json.loads(requests.get('https://api.telegram.org/bot'+str(os.getenv('TELEGRAM_BOT_TOKEN'))+'/getUpdates').text)


def create_telegram_integration(username):
    for update in updates['result']:
        if 'username' in update['message']['from']:
            if update['message']['from']['username'] == username:
                chat_id=update['message']['from']['id']
                return chat_id
            else:
                return "Please ping the bot"
        else:
            continue

def alert(chat_id, ctx):
    if ctx['check'].name:
        body = "Check %s with code %s has gone %s" % (
        ctx['check'].name, ctx['check'].code, ctx['check'].status)
    else:
        body = "Check with code %s has gone %s" % (ctx['check'].code, ctx['check'].status)
    bot.send_message(chat_id, body)
