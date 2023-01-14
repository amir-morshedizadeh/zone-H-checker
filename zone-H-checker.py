'''
Author: Amir Morshedizadeh
Email: morshedizadeh@gmail.com
'''

import io
import os
import time
import re
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from pil import Image
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import threading
import telegram.error
from telegram.error import NetworkError, Unauthorized
import ast
import logging
from watchgod import watch


# Telegram Bot config
"""
I used Bale as my messenger. Bale Messenger uses Telegram API.
You could use Telegram just by replacing api.telegram.org instead of tapi.bale.ai in the following lines
"""
bot = telegram.Bot(token='PUT-YOUR-TELEGRAM-TOKEN-HERE', base_url="https://tapi.bale.ai/")
telegram_token_zone_h = "PUT-YOUR-TELEGRAM-TOKEN-HERE"
telegram_group_id_zone_h = "PUT-YOUR-TELEGRAM-GROUP-ID-HERE"
telegram_api_sendphoto = f"https://tapi.bale.ai/bot{telegram_token_zone_h}/SendPhoto?chat_id="
telegram_api_sendmessage = f"https://tapi.bale.ai/bot{telegram_token_zone_h}/SendMessage"

# make your own regex for "domains_regex".
domains_regex = re.compile(r"([\w\d\-\.]*[\w\d\-]+\.com(\/.*)?)")

ua = UserAgent()
update_id = None
time_regex = re.compile(r"(\d+):(\d+)")
captcha_re = re.compile(r'^[A-Za-z0-9]+$')
headers = {'User-Agent': ua.random}
headers1 = {'User-Agent': ua.random,
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate',
'Origin': 'http://www.zone-h.org',
'Connection': 'keep-alive',
'Referer': 'http://www.zone-h.org/archive'}

# Bot Class
class mybot:
    global update_id
    def echo(self, bot):
        # Echo the message the user sent.
        global update_id
        # Request updates after the last update_id
        try:
            for update in bot.get_updates(offset=update_id, timeout=25):
                update_id = update.update_id + 1
                # Save entered captcha string on the "captcha.txt"
                if update.message:
                    x = str(update.message)
                    x = ast.literal_eval(x)
                    if captcha_re.match(x["text"]):
                        print(x["text"])
                        with open('captcha.txt', 'w', encoding='utf-8') as file:
                            file.write(x["text"])
                        return None
        except BaseException as e:
            print(e)
           
    def main(self):
        # Get the first pending update_id, this is so we can skip over it in case we get an "Unauthorized" exception.
        try:
            bot.delete_webhook()
            update_id = bot.get_updates()[0].update_id
        except IndexError:
            update_id = None
        #Enable logging
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                            level=logging.DEBUG)
        while True:
            try:
                mybot.echo(self, bot)
                time.sleep(2)
            except NetworkError:
                time.sleep(1)
            except Unauthorized:
                # The user has removed or blocked the bot.
                update_id += 1
    
    # Starting a thread for mybot Class
    def run(self):
        t1 = threading.Thread(target=self.main)
        t1.start()
        print(t1.getName)    

        
# Main Class
class main:
    def __init__(self, PHPSESSID, ZHE):
        self.Url = None
        self.PHPSESSID = PHPSESSID
        self.ZHE = ZHE

    def requests_retry_session(self, retries=3, session=None):
        session = session or requests.Session()
        try:
            retry = Retry(
                total=3,
                read=2,
                connect=5,
                backoff_factor=1
            )
            adapter = HTTPAdapter(max_retries=retry)
            session.mount('http://', adapter)
            session.mount('https://', adapter)
            return session
        except ValueError as err:
            print(err)

    # Saving results from zone-h.org to "Results.txt".
    def save(self, x):
        try:
            with open(results, 'a+') as file:
                file.write(x+'\n')
        except ValueError as err:
            print(err)

    # Extracting domain name and time of hack from zone-h.org.
    def get_assets(self, soup):
        rows = soup.find_all('tr')
        all_results = []
        for row in rows:
            tmp = row.get_text()
            domains = re.findall(domains_regex, tmp)
            times = re.findall(time_regex, tmp)
            for clock in times:
                for domain in domains:
                    domain = domain[0]
                    clock = " ".join(clock)
                    clock = clock.replace(" ", ":")
                    result = clock + " ----> " + domain
                    all_results.append(result)
        return all_results

    # Sending request to zone-h.org and analyzing the response.
    def request(self, url):
        try:
            session = self.requests_retry_session()
            response = session.get(url=url, cookies=cookies, headers=headers1)
            session.close()
        except ValueError as err:
            print(err)

        # Checking if captcha is required.
        while '''<input type="text" name="captcha"''' in response.text:
            try:
                print('Captcha')
                session = self.requests_retry_session()
                # Saving the captcha image on the disk and sending it to the messenger.
                img = session.get('http://www.zone-h.org/captcha.py')
                img = io.BytesIO(img.content)
                img = Image.open(img)
                img.save("captcha.png")
                files = {'photo': open('captcha.png', 'rb')}
                r = session.post(telegram_api_sendphoto, data={'chat_id': telegram_group_id_zone_h, 'caption': 'Please type what you see!'}, files=files)
                print('Trying to send captcha image to Bale ' + str(r))
                # Reading the captcha from captcha.txt and sending it to zone-h.org.
                print('Waiting for entering the captcha!')
                def watchgod_file(self):
                    with open('captcha.txt', 'r') as file:
                        captcha_txt = file.read().encode(encoding='utf-8', errors='ignore')
                        captcha_txt = {'captcha': captcha_txt}
                        print('Captcha inside the file is: ' + str(captcha_txt))
                        r1 = session.post(self.Url, data=captcha_txt, cookies=cookies, headers=headers1)
                        print('Trying to send the captcha to Zone-h.org: ' + str(r))
                        if '''<input type="text" name="captcha"''' in r1.text:
                            response = session.get(url=url, cookies=cookies, headers=headers1)
                        else:
                            return
                for changes in watch('captcha.txt'):
                    print(changes)
                    watchgod_file(self)
                    break
                break
            except ValueError as err:
                print(err)
        # Checking for cookie validation, if new cookie is set, write it manually inside .PHPSESSID and .ZHE files.
        if '''<html><body>-<script type="text/javascript"''' in response.text:
            print('Maybe Error PHPSESSID && ZHE')
        else:
            # getting the soup from the page and pass it to get_assets().
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

    # Sending new alerts to the messenger and writing it down to "Results.txt".
    def send_to_messenger(self, all_results):
        if all_results is not None:
            with open(results) as file:
                lines = file.readlines()
                try:
                    for x in all_results:
                        if x+'\n' in lines:
                            print(x + ' is duplicated')
                        else:
                            self.save(x)
                            session = self.requests_retry_session()
                            match0 = re.findall(domains_regex, x)
                            if match0:
                                for url in match0:
                                    site = url[0]
                                    match_clock = re.findall(time_regex, x)
                                    for clock in match_clock:
                                        clock = " ".join(clock)
                                        clock = clock.replace(" ", ":")
                                        msg = "++++++++++++++++++++++++\n" \
                                          "**Important alert from ZONE-H:** https://www.zone-h.org/archive \nAttack Time:   " + \
                                              clock + "\nAttacked Site:  " + site + "\n++++++++++++++++++++++++"
                                        content = {'chat_id': telegram_group_id_zone_h, 'text': msg}
                                        response = session.get(telegram_api_sendmessage, json=content, cookies=cookies,
                                                               headers=headers, allow_redirects=True)
                                        print(clock + site + ' is being sent to the group ' + str(response))
                                        time.sleep(2)
                except ValueError as err:
                    print(err)
        else:
            pass
    '''
    Getting number of pages and sending each page to request() then get_assets() to make a soup,
    then sending the soup to send_to_messenger() for final the decision for sending it to the messenger or alerting it as duplicated
    '''
    def setup(self, soup):
        tmp_list = []
        page_numbers = soup.find('td', class_='defacepages')
        if page_numbers and page_numbers.contents:
            for page_ in page_numbers:
                if not (page_ == '\n' or page_ == ' '):
                    tmp_list.append(page_)
            length = len(tmp_list)
            print("Total Pages of today in zone-h.org: ", length)
            j = 0
            while j <= length:
                try:
                    j += 1
                    self.Url = 'http://www.zone-h.org/archive/page=' + str(j)
                    soup = self.request(self.Url)
                    soup = self.get_assets(soup)
                    self.send_to_messenger(soup)
                    time.sleep(1)
                except ValueError as err:
                    print(err)

    # Looping forever.
    def start(self):
        while True:
            try:
                self.Url = 'http://www.zone-h.org/archive'
                print("Starting")
                soup = self.request(self.Url)
                self.setup(soup)
                print("Waiting 180s for re-scraping")
                time.sleep(108)
            except ValueError as err:
                print(err)
    
    # Starting a thread for Main Class
    def run(self):
        try:
            t2 = threading.Thread(target=self.start)
            t2.start()
            print(t2.getName)
        except ValueError as err:
            print(err)

if __name__ == '__main__':
    try:
        if os.path.isfile('captcha.txt'):
            pass
        else:
            open('captcha.txt', 'w+')

        if os.path.isfile('Results.txt'):
            results = os.path.basename('Results.txt')
            results = str(results)
        else:
            results = open('Results.txt', 'w+')

        if os.path.isfile('.PHPSESSID'):
            PHPSESSID = open('.PHPSESSID', 'r').read().strip()
        else:
            PHPSESSID = ''

        if os.path.isfile('.ZHE'):
            ZHE = open('.ZHE', 'r').read().strip()
        else:
            ZHE = ''
        cookies = {'PHPSESSID': PHPSESSID, 'ZHE': ZHE}
        e = mybot()
        e.run()
        d = main(PHPSESSID, ZHE)
        d.run()
    except ValueError as err:
        print(err)
