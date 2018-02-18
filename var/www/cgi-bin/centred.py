#!/usr/bin/env python3

"""
The MIT License (MIT)

Copyright (c) 2014 RaspiBO (started by dave4th)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

"""
Note:
- Ho preferito predisporre una funzione di decodifica "bytes -> str",
  molti dei dati restituiti dai comandi Redis infatti sono in questo
  formato, incompatibile ed inutilizzabile con tutto il resto
        b'testo'

"""

import time,os,shutil,redis
import sys      # mi serve per sys.exit() da togliere quando avro` finito di usarli
# se non servira` per altro ..

# Questa mi serve per avere piu` "istanze" della funzione che invia i messaggi,
# nel caso ve ne siano piu` d'uno da inviare in contemporanea (ma diversi fra loro)
from threading import Thread

# MyDB
import fls


# Attenzione perche` ci sono due send_message nelle librerie XMPP e MAIL
# comunque non dovrebbero infastidirsi

## Queste servono per XMPP ##
#from getpass import getpass
from pyxmpp2.simple import send_message

## Queste servono per la mail ##
# Import smtplib for the actual sending function
import smtplib
# Import the email modules we'll need
from email.mime.text import MIMEText

def SendMessageXMPP (User,Pass,To,Message):
    send_message(User,Pass,To,Message)

def SendMessageMail (User,Pass,ServerMail,Port,From,To,Subject,Message):
    Msg = MIMEText(Message)
    Msg['Subject'] = Subject
    Msg['From'] = From
    Msg['To'] = To
    # Send the message via SMTP server
    # La procedura e` testata con (google/gmail)
    ServerSMTP = smtplib.SMTP(ServerMail+":"+Port)
    ServerSMTP.starttls()
    ServerSMTP.login(User,Pass)
    ServerSMTP.send_message(Msg)
    ServerSMTP.quit()

def InviaMessaggi(NewMsg,Attempts,Delay):
    PhoneCheck = Attempts       # Mi serve sapere quanto vale Attempts per fare il controllo sull'autodial
    while Attempts > 0 and MyDB.exists(NewMsg): # Finche` tentativi > 0 ed il messaggio e` presente
        # Trovo il tipo di messaggio
        MsgType = MyDB.hget(NewMsg,"type")
        # Trovo la relativa lista di distribuzione, puo` essercene solamente una, ma forse e` meglio prevederne  di piu` ?
        MsgTypeList = MyDB.keys(Decode(MsgType)+"*")    # Pero` aspetta, questa contiene l'array .. o no ? per es.: alarm* = alarm:list
        for i in range(len(MsgTypeList)):       # Splitta l'array, che comunque e` a singolo valore, quindi "i" sempre = "0"
            Lista = Decode(MsgTypeList[i])      # Decodifica lista {name}:list
            for j in range(MyDB.llen(Lista)):  # Per ogni valore della lista di "alarm:list" o "alert:list" ovvero {name}:list
                if Decode(MyDB.lindex(Lista,j)) == "list:sip" and PhoneCheck == Attempts :      # Attiva solo una volta
                    for k in range(MyDB.llen("list:sip")):     # per ogni destinatario
                        # Qua potrebbe esserci l'inghippo, quando capitano due messaggi d'allarme
                        # contemporaneamente, uno dei due potrebbe non essere inviato ..
                        # mi sa che bisognera` provare, teoricamente il problema dovrebbe essere
                        # solo per "alarm.wav", perche` "autodial" e` sempre uguale.
                        #
                        # Preparo le variabili per la creazione del file "autodial" per asterisk
                        Channel = "Channel: SIP/"+Decode(MyDB.lindex("list:sip",k))
                        Callerid = "Callerid: Alarm"
                        MaxRetries = "MaxRetries: "+str(Attempts)
                        RetryTime = "RetryTime: "+str(Delay*60)
                        WaitTime  = "WaitTime: 45"
                        Context = "Context: centred"
                        Extension = "Extension: 10"
                        Priority = "Priority: 1"
                        FileDial = open("autodial","w")
                        FileDial.write(Channel+"\n")
                        FileDial.write(Callerid+"\n")
                        FileDial.write(MaxRetries+"\n")
                        FileDial.write(RetryTime+"\n")
                        FileDial.write(WaitTime+"\n")
                        FileDial.write(Context+"\n")
                        FileDial.write(Extension+"\n")
                        FileDial.write(Priority+"\n")
                        FileDial.close()
                        # alarm.wav
                        FileAlarm = open("alarm.txt","w")
                        FileAlarm.write(Decode(MyDB.hget(NewMsg,"desc")))
                        FileAlarm.close()
                        #os.system("text2wave -F 8000 -eval \"(language_italian)\" -otype wav -o /usr/share/asterisk/sounds/en/alarm.wav alarm.txt")
                        # ho dovuto mettere pc invece di lp, sem,bra che la voce femminile non funzioni piu` Sun 18 Feb 2018 10:35:47 AM CET
                        os.system("text2wave -F 8000 -eval \"(voice_pc_diphone)\" -scale 1 -otype wav -o /usr/share/asterisk/sounds/en/alarm.wav alarm.txt")
                        shutil.copyfile("autodial","/var/spool/asterisk/outgoing/autodial")
                if Decode(MyDB.lindex(Lista,j)) == "list:xmpp":
                    for k in range(MyDB.llen("list:xmpp")):     # per ogni destinatario
                        # Meglio che componga il messaggio "prima", poi, chissenefrega .. metto tutto insieme, il problema e` che non so come funziona
                        User = Decode(MyDB.hget("account:xmpp","username"))
                        Pass = Decode(MyDB.hget("account:xmpp","password"))
                        To = Decode(MyDB.lindex("list:xmpp",k))
                        Messaggio = MyDB.hgetall(NewMsg)        # Non sono riuscito ad utilizzare HMGET, non ho capito come si fa`.
                        SendMessageXMPP(User,Pass,To,Messaggio)
                if Decode(MyDB.lindex(Lista,j)) == "list:mail" :
                    for k in range(MyDB.llen("list:mail")):
                        User = Decode(MyDB.hget("account:mail","username"))
                        Pass = Decode(MyDB.hget("account:mail","password"))
                        ServerMail = Decode(MyDB.hget("account:mail","serversmtp"))
                        Port = Decode(MyDB.hget("account:mail","port"))
                        From = Decode(MyDB.hget("account:mail","mailfrom"))
                        To = Decode(MyDB.lindex("list:mail",k))
                        Subject = Decode(MyDB.hget(NewMsg,"desc"))
                        Message = MyDB.hgetall(NewMsg)
                        SendMessageMail (User,Pass,ServerMail,Port,From,To,Subject,str(Message))        # Notare str()
        Attempts = Attempts - 1
        time.sleep(Delay * 60)      # Trasformo in secondi

# Faccio una funzione per la decodifica bytes -> str
def Decode(TxT):
    return TxT.decode('unicode_escape')


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Da qua in avanti le operazioni sono da eseguire in ciclica
while True:
    Msg = MyDB.keys("msg:*")	# Leggo se ci sono messaggi
    if len(Msg) > 0:
        for i in range(len(Msg)):
            NewMsg = "new:"+Decode(Msg[i])
            if MyDB.renamenx(Decode(Msg[i]),NewMsg): # Lo rinomino per spostarlo, solo se non esiste gia`
                # Se gia` esiste, rimarra` in coda per essere rinominato ..
                #
                # Poi devo lanciare un funzione che pero` funzioni come thread e vada poi avanti da sola
                #                 Key, Tentativi d'invio            , Ritardo fra gli invii
                #FUNZIONETHREAD(NewMsg,int(Decode(MyDB.hget("config","attempts"))),int(Decode(MyDB.hget("config","delay"))))
                #
                # Vediamo se ho capito come si usa il threading ...
                t = Thread(target=InviaMessaggi, args=(NewMsg,int(Decode(MyDB.hget("config","attempts"))),int(Decode(MyDB.hget("config","delay")))))
                t.start()
    time.sleep(int(Decode(MyDB.hget("config","tcycle"))))      # ritardo prima di un successivo controllo allarmi, leggo il tempo dalla configurazione
