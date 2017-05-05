#Cyrus Boushehri 4/5/17
import socket

server  = "localhost"                                          #Global settings
port    = 6667
lang    = ["#test", "#test2"]
botnick = "Tanobb"
irc     = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

irc.connect((server, port))                                    #Connect to server
irc.send(bytes("USER "+botnick+" "+botnick+" "+botnick+" "+botnick+"\n", "UTF-8"))
irc.send(bytes("NICK "+botnick+"\n", "UTF-8"))

def sendmsg(msg, target):                                      #Send messages
    irc.send(bytes("PRIVMSG "+target+" :"+msg+"\n", "UTF-8"))

def translate(msg):                                            #Translation (placeholder)
    return msg

for i in lang:                                                 #Join channels
    irc.send(bytes("JOIN "+lang[0]+"\n", "UTF-8"))
    irc.send(bytes("JOIN "+lang[1]+"\n", "UTF-8"))
    
while 1:
    ircmsg = irc.recv(2048).decode("UTF-8")                    #Get input
    ircmsg = ircmsg.strip('\n\r')
    
    print(ircmsg) #debug
    
    if ircmsg.find("PING :") != -1:                            #Respond to server pings
        irc.send(bytes("PONG :pingis\n", "UTF-8"))
        
    if ircmsg.find("PRIVMSG") != -1:                           #Listen for messages
        name = ircmsg.split('!',1)[0][1:]
        chan = ircmsg.split('#')[1].split(' :')[0]
        msg  = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
        tr   = translate(msg)
        
        sendmsg("<"+name+"> "+tr+"", "#"+chan)