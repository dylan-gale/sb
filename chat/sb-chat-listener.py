import json
import requests
from lxml import html
import socket
import re
 
#we set up the URLs we're gonna need
URL_AUTH = "https://www.saltybet.com/authenticate?signin=1"
URL_STATS = "http://www.saltybet.com/ajax_get_stats.php"
URL_MAIN = "http://www.saltybet.com"
 
#open a session and authenticate to saltybet
session_requests = requests.session()
 
result = session_requests.get(URL_AUTH)
tree = html.fromstring(result.text)
signin = list(set(tree.xpath("//input[@name='authenticate']/@value")))[0]
 
AUTH = {"email": "dyylangale@gmail.com", "pword": "gylanghjk", "authenticate": signin}
 
result = session_requests.post(URL_AUTH, data = AUTH, headers = dict(referer = URL_AUTH))
 
 
#we set up the twitch stuff
HOST = "irc.twitch.tv"
PORT = 6667
NICK = "69420dylan42069"
PASS = 'oauth:x7qg6rp0dsg9l6w86kuy8kk8j6h1a9'
 
#we probably won't ever need the bot to send a message but whatever here it is
def send_message(message):
    s.send(bytes("PRIVMSG #" + NICK + " :" + message + "\r\n", "UTF-8"))
 
s = socket.socket()
s.connect((HOST, PORT))
s.send(bytes("PASS " + PASS + "\r\n", "UTF-8"))
s.send(bytes("NICK " + NICK + "\r\n", "UTF-8"))
s.send(bytes("JOIN #saltybet" + " \r\n", "UTF-8"))
 
def getUser(line):
    separate = line.split(":")
    user = separate[1].split("!")[0]
    return user
def getMessage(line):
    separate = line.split(":")
    message = ""
    if "QUIT" not in separate[1] and "JOIN" not in separate[1] and "PART" not in separate[1]:
        message = separate[2][:len(separate[2])]
    return message
 
#we open or initialize the data set so we can start adding to it
data = {}
 
def main():
    readbuffer = ""
    new_data = {}
    streak_table = json.dumps({})
    i=0
    while True:
        readbuffer = readbuffer + str(s.recv(1024))
        temp = readbuffer.split("\\r\\n")
        readbuffer = temp.pop()
        
        for line in temp:
            #print(line)
 
            if "PING" in line:
                s.send(bytes("PONG \r\n", "UTF-8"))
                send_message("/w casey666666 you want a job m8")
                print(line)
                #s.send(line.replace("PING", "PONG").encode())
                continue
                

            if "tmi.twitch.tv" in getUser(line):
                continue

            if getUser(line).upper() not in [ "WAIFU4U", "NIGHTBOT", "MOOBOT", "SALTYBOT"]:
                if "@" not in getMessage(line):            
                    print(getMessage(line))
main();
