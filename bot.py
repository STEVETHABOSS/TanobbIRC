#Cyrus Boushehri 4/5/17

import socket

server  = "localhost"                                          #Settings
port    = 6667
channel = "#test"
botnick = "Tanobb"
ircsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

ircsock.connect((server, port))                                #Connect to server

ircsock.send(bytes("USER "+botnick+" "+botnick+" "+botnick+ " " +botnick+ "\n", "UTF-8")) #Bot information
ircsock.send(bytes("NICK "+botnick+"\n", "UTF-8"))


def joinchan(channel):                                         #Join Channel
    ircsock.send(bytes("JOIN "+ channel +"\n", "UTF-8"))

    ircmsg = ""
    while ircmsg.find("End of /NAMES list.") == -1:
        ircmsg = ircsock.recv(2048).decode("UTF-8")
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)

def ping():                                                    #Respond to server Pings
    ircsock.send(bytes("PONG :pingis\n", "UTF-8"))

def sendmsg(msg, target=channel):                              #Send messages
    ircsock.send(bytes("PRIVMSG "+ target +" :"+ msg +"\n", "UTF-8"))

def main():
    joinchan(channel)
    
    while 1:
        
        ircmsg = ircsock.recv(2048).decode("UTF-8")            #Strip formatting from input
        ircmsg = ircmsg.strip('\n\r')
        print(ircmsg)
        
        if ircmsg.find("PING :") != -1:                        #Listen for pings
            ping()
        
        if ircmsg.find("PRIVMSG") != -1:                       #Listen for messages
            name    = ircmsg.split('!',1)[0][1:]
            message = ircmsg.split('PRIVMSG',1)[1].split(':',1)[1]
            
            if message.find('Hi ' + botnick) != -1:
                sendmsg("Hello " + name + "!")
            
            if message[:5].find('.tell') != -1:
                target = message.split(' ', 1)[1]
            
                if target.find(' ') != -1:
                    message = target.split(' ', 1)[1]
                    target = target.split(' ')[0]
            
                else:
                    target = name
                    message = "Could not parse. The message should be in the format of ‘.tell [target] [message]’ to work properly."
        
                sendmsg(message, target)

main()
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            
            