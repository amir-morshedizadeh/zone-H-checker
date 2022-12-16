#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import re
from time import sleep
import telegram.error
from telegram.error import NetworkError, Unauthorized
import ast

update_id = None
captcha_re = re.compile(r'^[A-Za-z0-9]+$')


def main():
    """Run the bot."""
    global update_id
    # Telegram Bot Authorization Token
    bot = telegram.Bot(token='PUT-YOUR-TOKEN-HERE',
                       base_url="TELEGRAM-or-BALE-API-ADDRESS")

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        bot.delete_webhook()
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    # Enable logging
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)

    while True:
        try:
            echo(bot)
            sleep(2)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def echo(bot):
    """Echo the message the user sent."""
    global update_id
    # Request updates after the last update_id
    try:
        for update in bot.get_updates(offset=update_id, timeout=25):
            update_id = update.update_id + 1

            if update.message:  # Save entered captcha string on the "captcha.txt"
                x = str(update.message)
                x = ast.literal_eval(x)
                if captcha_re.match(x["text"]):
                    print(x["text"])
                    with open('captcha.txt', 'w', encoding='utf-8') as file:
                        file.write(x["text"])
    except BaseException as e:
        print(e)



if __name__ == '__main__':
    main()
