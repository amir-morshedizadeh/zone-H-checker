# zoneH_checker
It checks "www.zone-h.org/archive" and looks for your domain, if your assets were in the list, it sends the log to your Telegram/Bale group.

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
![image](https://user-images.githubusercontent.com/83567836/206893416-305562ae-3dc8-40c5-a134-2f5806bf93f7.png)

3- Through your browser navigate to https://www.zone-h.org/archive,
then press F12 to see your cookie to write PHPSESSID value to .PHPSESSID file and ZHE value to .ZHE file in the script path
![image](https://user-images.githubusercontent.com/83567836/206893340-773d844c-bc31-4975-aee8-cb5fbb1b6715.png)

4- Make a regex to cover all your domains and replace it with the value of current regex
![image](https://user-images.githubusercontent.com/83567836/206894505-f42a81fa-ab39-4d45-ad5f-d24629300f4b.png)

