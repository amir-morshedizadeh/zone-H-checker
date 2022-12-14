# zone-H-checker
It checks "www.zone-h.org/archive" and looks for your domain, if your assets found in the list, it sends the alert to your Telegram/Bale group.
It also sends captcha image of zone-h.org to your Telegram group in order to enter the captcha text to continue for looking.

# Installation
Python >= 3.9
```
git clone https://github.com/amir-morshedizadeh/zone-H-checker.git
pip3 install -r requirements.txt
```

# Configuration
1- At first make a Telegram Bot or Bale Bot and obtain your token:

###### Telegram:  [Telegram Bot](https://core.telegram.org/bots#how-do-i-create-a-bot)
###### Bale:  [Bale Bot](https://dev.bale.ai/quick-start)

2- Make a group in Telegram/Bale then write your token and group id in the following portion of the code:
![image](https://user-images.githubusercontent.com/83567836/210405957-01ca30e4-cbeb-49c6-a99d-d195a791943a.png)

3- Through your browser navigate to https://www.zone-h.org/archive,
then press F12 to see your cookie to write PHPSESSID value to .PHPSESSID file and ZHE value to .ZHE file in the script path.
![image](https://user-images.githubusercontent.com/83567836/206893340-773d844c-bc31-4975-aee8-cb5fbb1b6715.png)

4- Make a regex to cover all your domains and replace it with the value of current regex.
![image](https://user-images.githubusercontent.com/83567836/206894505-f42a81fa-ab39-4d45-ad5f-d24629300f4b.png)

5- Run the program and monitor the Telegram group for any incoming alerts and also solving the captcha.
