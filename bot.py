#Cyrus Boushehri 4/5/17
import socket

server  = "localhost"                                          #Global settings
port    = 6667
channel = ["#ar", "#de", "#en", "#es", "#fa", "#fi", "#fr", "hi", "#ja", "#ko", "#pt", "#ru", "#zh"]
botnick = "Tanobb"
irc     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((server, port))                                    #Connect to server
irc.send(bytes("USER {0} {0} {0} {0}\n".format(botnick), "UTF-8"))
irc.send(bytes("NICK {}\n".format(botnick), "UTF-8"))

def sendmsg(msg, chan):                                        #Send messages
    irc.send(bytes("PRIVMSG {} :{}\n".format(chan, msg), "UTF-8"))

def translate(msg):                                            #Translation (placeholder)
    return msg

for i in channel:                                              #Join channels
    irc.send(bytes("JOIN {}\n".format(i), "UTF-8"))

while 1:
    ircmsg = irc.recv(2048).decode("UTF-8")                    #Get input
    ircmsg = ircmsg.strip('\n\r')
    
    if ircmsg.find("PING :") != -1:                            #Respond to server pings
        irc.send(bytes("PONG :pingis\n", "UTF-8"))
        
    if ircmsg.find("PRIVMSG") != -1:                           #Listen for messages
        name = ircmsg.split('!',1)[0][1:]
        chan = ircmsg.split('#')[1].split(' :')[0]
        msg  = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
        tr   = translate(msg)
        
        for i in channel:                                      #Send translated reply
            if i != "#"+chan:
                sendmsg("<{}> [{}] {} {}".format(name, chan, msg, tr), i)