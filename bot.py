#Cyrus Boushehri 4/5/17
import socket
from api_client import translate

server  = "localhost"                                          #Global settings
port    = 6667
channel = ["#ar", "#de", "#en", "#es", "#fa", "#fi", "#fr", "hi", "#ja", "#ko", "#pt", "#ru", "#zh-CHS"]
nick    = "Tanobb"
irc     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((server, port))                                    #Connect to server, send bot info
irc.send(bytes("USER {0} {0} {0} {0}\n".format(nick), "UTF-8"))
irc.send(bytes("NICK {}\n".format(nick), "UTF-8"))

for i in channel:                                              #Join all channels
    irc.send(bytes("JOIN {}\n".format(i), "UTF-8"))
    
while 1:
    ircmsg = irc.recv(2048).decode("UTF-8").strip("\n\r")      #Get input stream
    print(ircmsg)
    
    if ircmsg.find("PING :") != -1:                            #Respond to server pings
        irc.send(bytes("PONG :pingis\n", "UTF-8"))
        
    if ircmsg.find("PRIVMSG") != -1:                           #Listen for messages
        name = ircmsg.split('!',1)[0][1:]                      #Get name, channel and text from buffer
        lang = ircmsg.split('#')[1].split(' :')[0]
        msg  = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
        
        for chan in channel:                                                 #Send for all channels except the original
            if chan != "#"+lang:
                try:
                    tr = translate(chan.strip("#"), lang, msg)               #Call translate function
                except:
                    tr = "Translation Error"
                tex = "<{}> [{}] {} {}".format(name, lang, msg, tr)          #Format message: <name> [languange] untranslated text translated text
                irc.send(bytes("PRIVMSG {} :{}\n".format(chan, tex), "UTF-8"))