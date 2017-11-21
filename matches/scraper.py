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
 
#we probably wont ever need the bot to send a message but whatever here it is
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
 
#now we start phase one of data mining, the illuminati stats. we scrape this right after bets are open and return it as a JSON object.
def illuminati_scrape():
    sb = session_requests.get(URL_STATS, headers = dict(referer = URL_STATS))
    return sb.json();
 
#now for phase two, after betting ends but before the fight.
#THIS DOESN'T WORK AT ALL RIGHT NOW
def odds_scrape(message):
    #this is dumb and hacky
    ratio = [0,0,0]
    i=0
    #use regex to find the total bets for each fighter
    odds = re.findall(r'(?<=\$)[\d\,]*', message)
    for odd in odds:
        #remove commas and cast to int
        ratio[i] = int("".join(odd.split(",")));
        i += 1
    #return a ratio of the two, rounded to 4 decimal places
    return round(ratio[0]/ratio[1], 4);
 
 
#last is phase three, after the winner is declared but before the next fight.
#this is when we stitch together the whole JSON entry
def winner_scrape(message):
    if "Payouts to Team Red" in message:
        return 0;
    else:
        return 1;
   
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
            if "PING" in line:
                s.send(bytes("PONG \r\n", "UTF-8"))
                #s.send(bytes(line.replace("PING", "PONG") + "\r\n", "UTF-8"))
                continue
            if getUser(line).upper() == "WAIFU4U":
                if "Bets are OPEN" in getMessage(line):
                    new_data = illuminati_scrape();
                elif "Bets are locked" in getMessage(line):
                    new_data.update({'odds':odds_scrape(line)});
                elif "Payouts to Team" in getMessage(line):
                    new_data.update({'winner':winner_scrape(line)});
                    print(list(new_data.values()), '\n');
 
main();
