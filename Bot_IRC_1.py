import socket, sys, math, time

###################################################
### VARIABLES À MODIFIER ##########################
host="XXX"
port=XXXX
canal="XXX"
bot="XXX"
nickname="XXX"
mdp="XXX"
s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
###################################################

###################################################
### CONNEXION (voir RFC 1459) #####################
s.connect((host,port))
s.send("PASS " + mdp + "\r\n")
s.send("NICK " + nickname + "\r\n") 
s.send("USER " + nickname + " " + nickname + " " + nickname + " TEST \r\n")
s.send("JOIN " + host + " \r\n")

time.sleep(1)
###################################################


###################################################
### PARCOURS DU FLUX ##############################
while 1:
    reponse=s.recv(2040)
    print(reponse)
    
    if reponse.find("PING")!=-1:
        s.send("PONG " + str(reponse.split()) + "\r\n")
        print "PONG OK"

    if reponse.find("396")!=-1:
        s.send("PRIVMSG " + bot + " : !ep1 \r\n")
        reponse2=s.recv(2040)
        reponse_formatee=(reponse2.strip("\r\n").split(":"))[2].split("/")
        nb1=int(reponse_formatee[0])
        nb2=int(reponse_formatee[1])
        resultat=round(math.sqrt(nb1)*nb2, 2)
        s.send("PRIVMSG " + bot + " :!ep1 -rep " + str(resultat) + "\r\n")
        print(s.recv(2040))
###################################################       

	
