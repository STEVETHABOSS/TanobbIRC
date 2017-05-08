#Cyrus Boushehri 4/5/17
import socket
from api_client import translate

server  = "localhost"                                              #Global settings
port    = 6667
channel = ["#ar", "#de", "#en", "#es", "#fa", "#fi", "#fr", "hi", "#ja", "#ko", "#pt", "#ru", "#zh-CHS"]
nick    = "Tanobb"
irc     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
msg     = {"name":"","lang":"","text":""}

irc.connect((server, port))                                        #Connect to server, send bot info
irc.send(bytes("USER {0} {0} {0} {0}\n".format(nick), "UTF-8"))
irc.send(bytes("NICK {}\n".format(nick), "UTF-8"))

def format(input):
    msg["name"] = input.split('!',1)[0][1:]                        #Get name, channel and text from buffer
    msg["lang"] = input.split('#')[1].split(' :')[0]
    if input.find("PRIVMSG") != -1:
        msg["text"]  = input.split('PRIVMSG',1)[1].split(':',1)[1]
    return(msg)


def broadcast(name, lang, text):
    for chan in channel:                                           #Send for all channels except the original
        if chan != "#"+lang:
            try:
                tr = translate(chan.strip("#"), lang, text)        #Call translate function
            except:
                tr = "Translation Error"
            form = "{} {} {} {}".format(name, lang, text, tr)      #Format message: <name> [languange] untranslated text translated text
            irc.send(bytes("PRIVMSG {} :{}\n".format(chan, form), "UTF-8"))
            
            
for i in channel:                                                  #Join all channels
    irc.send(bytes("JOIN {}\n".format(i), "UTF-8"))
    
while 1:
    ircmsg = irc.recv(2048).decode("UTF-8").strip("\n\r")          #Get input stream
    print(ircmsg)
    
    if ircmsg.find("PING :") != -1:                                #Respond to server pings
        irc.send(bytes("PONG :pingis\n", "UTF-8"))
        
    if ircmsg.find("PRIVMSG") != -1:                               #Listen for messages
        res = format(ircmsg)
        broadcast(res["name"], res["lang"], res["text"] )
        
    if (ircmsg.find("JOIN") != -1) and ircmsg.find("Tanobb"):
        res = format(ircmsg)
        broadcast("", "", "{} has joined #{}".format(res["name"], res["lang"]))
        print("!!!! JOIN !!!!")
        
    if ircmsg.find("QUIT") != -1:
        res = format(ircmsg)
        broadcast("", "", "{} has quit #{}".format(res["name"], res["lang"]))
        print("!!!! QUIT !!!!")