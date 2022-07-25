import socket
import random
from threading import Thread
from datetime import datetime
from colorama import Fore, init, Back
from json import loads

init()
colors = [Fore.BLUE, Fore.CYAN, Fore.GREEN, Fore.LIGHTBLACK_EX, Fore.LIGHTBLUE_EX, Fore.LIGHTCYAN_EX, Fore.LIGHTGREEN_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTRED_EX, Fore.LIGHTWHITE_EX, Fore.LIGHTYELLOW_EX, Fore.MAGENTA, Fore.RED, Fore.WHITE, Fore.YELLOW]

global alphabet
global ralphabet
global keynum
global numchars

with open('alphabet.json', 'r') as f:
    alphabet = loads(f.read())

ralphabet = {}
keynum = []

numchars = 1

for x in alphabet:
    ralphabet[numchars] = x
    numchars = numchars + 1

numchars = numchars - 1

client_color = random.choice(colors)
SERVER_HOST = 'ee.sly.io'
SERVER_PORT = 41775
separator_token = 'G2jeZf1JJmBSRrCDD2xmyMCT'
channel_token = '_W0rGIrrpjf0CyKPiBgb110zEEP17pmMvx8WraQWr4ACF1ihVjMI0i3OzrQGBz93m'
channel = 'DEFAULT' + channel_token
connected = True

s = socket.socket()
print('[*] Connecting to {}:{}...'.format(SERVER_HOST, SERVER_PORT))
s.connect((SERVER_HOST, SERVER_PORT))
print('[+] Connected.')
name = input('[?] Enter your name: ')
key = input('[?] Enter the key: ')

for x in key:
    try:
        keynum.append(alphabet[x])
    except KeyError:
        print('[!] Unsupported character in key: {}, quitting'.format(x))
        quit()

def text_arr(text):
    arr = []
    for x in text:
        try:
            arr.append(alphabet[x])
        except KeyError:
            print('[!] Unsupported character in text, {} will not be included'.format(x))
    return(arr)

def decrypt(arr):
    keyindex = 0
    tempnum = 0
    output = []
    outstring = ''
    for x in arr:
        try:
            tempnum = x - keynum[keyindex]
            keyindex = keyindex + 1
            if tempnum < 1:
                tempnum = tempnum + numchars
            output.append(tempnum)
        except:
            keyindex = 0
            tempnum = x-keynum[keyindex]
            keyindex = keyindex + 1
            if tempnum < 1:
                tempnum = tempnum + numchars
            output.append(tempnum)
    for x in output:
        outstring = outstring + ralphabet[x]
    return(outstring)

def encrypt(arr):
    keyindex = 0
    tempnum = 0
    output = []
    outstring = ''
    for x in arr:
        try:
            tempnum = x + keynum[keyindex]
            keyindex = keyindex + 1
            if tempnum > numchars:
                tempnum = tempnum - numchars
            output.append(tempnum)
        except:
            keyindex = 0
            tempnum = x + keynum[keyindex]
            keyindex = keyindex + 1
            if tempnum > numchars:
                tempnum = tempnum - numchars
            output.append(tempnum)
    for x in output:
        outstring= outstring + ralphabet[x]
    return(outstring)

def listen_for_messages():
    while True:
        messageenc = s.recv(32768).decode()
        message = str(decrypt(text_arr(messageenc)))
        try:
            if channel in message:
                print('\n' + message.replace(separator_token, ': ').replace(channel, ''))
        except:
            print('[!] Message failed to decode.')
t = Thread(target = listen_for_messages)
t.daemon = True
t.start()

if connected:
    date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    to_send = '{}{}[{}] {} connected to the server{}'.format(channel, client_color, date_now, name, Fore.RESET)
    s.send(encrypt(text_arr(to_send)).encode())
    connected = False

while True:
    to_send =  input()
    if to_send.startswith('.channel'):
        channel = to_send.replace('.channel ', '').upper()+channel_token
        print('[i] Changed channel to {}'.format(channel.replace(channel_token, '')))
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = '{}{}[{}] {} joined the channel{}'.format(channel, client_color, date_now, name, Fore.RESET)
        s.send(encrypt(text_arr(to_send)).encode())
    elif to_send.startswith('.quit'):
        qq = input('[?] Do you want to quit? (Y/N): ').upper()
        if qq == 'Y':
            break
        else:
            pass
    else:
        date_now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        to_send = '{}{}[{}] {}{}{}{}'.format(channel, client_color, date_now, name, separator_token, to_send, Fore.RESET)
        s.send(encrypt(text_arr(to_send)).encode())

s.close()