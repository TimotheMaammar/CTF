import socket, sys, math, time, base64, zlib

###################################################
### VARIABLES A MODIFIER ##########################
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
        s.send("PRIVMSG " + bot + " : !ep4 \r\n")
        reponse2=s.recv(2040)
        resultat = str(reponse2.split(":")[2])
        base64_bytes = resultat.encode('ascii')
        message_bytes = base64.b64decode(base64_bytes)
        final=zlib.decompress(message_bytes)  
        s.send("PRIVMSG " + bot + " :!ep4 -rep " + str(final) + "\r\n")
        print(s.recv(2040))
###################################################       

	
