"""
Author: Amir Morshedizadeh
Email: morshedizadeh@gmail.com
"""

import io
import os
from bs4 import BeautifulSoup
import re
import time
from urllib3.util.retry import Retry
import requests
from requests.adapters import HTTPAdapter
from pil import Image

telegram_token_zone_h = "PUT-YOUR-TELEGRAM-TOKEN-HERE"
telegram_group_id_zone_h = "PUT-YOUR-TELEGRAM-GROUP-ID-HERE"

"""
I used Bale as the messenger. It uses TELEGRAM API.
You can use Telegram by just replacing api.telegram.org instead of tapi.bale.ai in the following 2 lines
"""
telegram_api_sendphoto = f"https://tapi.bale.ai/bot{telegram_token_zone_h}/SendPhoto?chat_id="
telegram_api_sendmessage = f"https://tapi.bale.ai/bot{telegram_token_zone_h}/SendMessage"

#Make your own assets's regex to cover all your domains and subdomains
domains_regex = re.compile(r"([\w\d\-\.]*[\w\d\-]+\.ir(\/.*)?)")

time_regex = re.compile(r"(\d+):(\d+)")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36'}
headers1 = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Origin': 'http://www.zone-h.org',
            'Connection': 'keep-alive',
            'Referer': 'http://www.zone-h.org/archive',
            }


# Class
class main:
    def __init__(self, PHPSESSID, ZHE):
        self.Url = None
        self.PHPSESSID = PHPSESSID
        self.ZHE = ZHE

    def requests_retry_session(
            retries=3,
            session=None,
    ):
        session = session or requests.Session()
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


    # Saving results from zone-h.org to Results.txt
    def save(self, x):
        try:
            with open(results, 'a+') as file:
                file.write(x+'\n')
        except ValueError as err:
            print(err)

    # Extracting domain name and time of hack from zone-h.org
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

    # Sending request to zone-h.org and analyzing the response
    def request(self, url):
        try:
            session = self.requests_retry_session()
            response = session.get(url=url, cookies=cookies, headers=headers1)
            session.close()
        except ValueError as err:
            print(err)

        # Checking if captcha is required
        while '''<input type="text" name="captcha"''' in response.text:
            print('Captcha')
            session = self.requests_retry_session()

            # Saving the captcha image on the disk and sending it to the messenger
            img = session.get('http://www.zone-h.org/captcha.py')
            img = io.BytesIO(img.content)
            img = Image.open(img)
            img.save("captcha.png")
            files = {'photo': open('captcha.png', 'rb')}
            r = session.post(telegram_api_sendphoto, data={'chat_id': telegram_group_id_zone_h, 'caption': 'Please type what you see!\n30 seconds for entering the captcha!'}, files=files)
            print('Trying to send captcha image to Bale ' + str(r))

            # Reading the captcha from captcha.txt and sending it to zone-h.org
            print('Waiting 30s seconds for entering the captcha! ')
            time.sleep(30)
            with open('captcha.txt', 'r') as file:
                captcha_txt = file.read().encode(encoding='utf-8', errors='ignore')
                captcha_txt = {'captcha': captcha_txt}
                print('Captcha inside the file is: ' + str(captcha_txt))
                r1 = session.post(self.Url, data=captcha_txt, cookies=cookies, headers=headers1)
                print('Trying to send the captcha to Zone-h.org: ' + str(r))
                if '''<input type="text" name="captcha"''' in r1.text:
                    response = session.get(url=url, cookies=cookies, headers=headers1)
                else:
                    break

        # Checking for cookie validation, if new cookie is set, write it manually inside .PHPSESSID and .ZHE files
        if '''<html><body>-<script type="text/javascript"''' in response.text:
            print('Maybe Error PHPSESSID && ZHE')
        else:
            # Getting the soup from the page and pass it to get_assets()
            soup = BeautifulSoup(response.text, 'html.parser')
            return soup

    # Sending new alerts to the messenger and writing it down to Results.txt
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

    """
    Getting number of pages and sending each page to request() then get_assets() to make a soup,
    then sending the soup to send_to_messenger() for final the decision for sending it to the messenger or alerting it as duplicated
    """
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
                j += 1
                self.Url = 'http://www.zone-h.org/archive/page=' + str(j)
                soup = self.request(self.Url)
                soup = self.get_assets(soup)
                self.send_to_messenger(soup)
                time.sleep(1)

    # Looping forever
    def start(self):
        while True:
            self.Url = 'http://www.zone-h.org/archive'
            print("Starting")
            soup = self.request(self.Url)
            self.setup(soup)
            print("Waiting 300s for re-scraping")
            time.sleep(300)


# Main
if __name__ == '__main__':
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
    main = main(PHPSESSID, ZHE)
    main.start()
