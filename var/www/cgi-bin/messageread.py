#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()

# Faccio una funzione per la decodifica bytes -> str
def Decode(TxT):
    return TxT.decode('unicode_escape')


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
RedisKey = "msg"


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
#print (mhl.MyHtmlHead())
print ("""
<html>

<head>
  <title>Centralino sicurezza</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="centralino, sicurezza, allarme, python">
  <meta name="Author" content="Davide">
""")
Refresh = Decode(MyDB.hget("config","tcycle"))     # Aggiornamento/Reload pagina sincronizzato col tempo ciclo messaggi
print ("<meta http-equiv=\"refresh\" content=\""+Refresh+"\">")
print ("""
</head>

<body>
""")

# Force Reload button

print ("<table>")   # 3 colonne

print ("<tr>")
print ("<td>")
#print ("")
print ("</td>")
print ("<td>")
#print ("")
print ("</td>")
print ("<td>")
#print ("")
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td colspan=\"3\">")
#print ("<hr/>") # La linea orizzontale
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("")  # Testo nella 1a colonna
print ("</td>")
print ("<td>")
print ("<button type=\"button\" onclick='location.href=\"/cgi-bin/messageread.py\"'>Force Reload</button>")
print ("</td>")
print ("<td>")
print ("")  # Testo nella 3a colonna
print ("</td>")
print ("</tr>")

print ("</table>")
# End force reload


Msg = (MyDB.keys(RedisKey+"*"))  # msg:*
if len(Msg) != 0:       # Se ci sono messaggi da visualizzare ..
    print ("<h3>Nuovi messaggi<h3>")
    print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
    print ("<tr>")
    print ("<td>")
    print ("<b>Key</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Date</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Type</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Description</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Value</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>u.m.</b>")
    print ("</td>")
    print ("</tr>")
    for i in range(len(Msg)):
        print ("<tr>")
        print ("<td>")
        print (Decode(Msg[i]))
        print ("</td>")
        for j in ["date", "type", "desc", "value", "um"]:
            print ("<td>")
            print (Decode(MyDB.hget(Msg[i],j)))
            print ("</td>")
        print ("</tr>")
    print ("</table>")
    
    print ("<br>")
    print ("<br>")

Msg = (MyDB.keys("new:"+RedisKey+"*"))  # new:msg:*
if len(Msg) != 0:
    print ("<h3>Messaggi inviati/in invio<h3>")
    print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
    print ("<tr>")
    print ("<td>")
    print ("<b>Key</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Date</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Type</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Description</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Value</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>u.m.</b>")
    print ("</td>")
    print ("</tr>")
    for i in range(len(Msg)):
        print ("<tr>")
        print ("<td>")
        print (Decode(Msg[i]))
        print ("</td>")
        for j in ["date", "type", "desc", "value", "um"]:
            print ("<td>")
            print (Decode(MyDB.hget(Msg[i],j)))
            print ("</td>")
        print ("</tr>")
    print ("</table>")
    
    print ("<br>")
    
    print (mhl.MyActionForm("/cgi-bin/messagewrite.py","POST"))
    print ("<table>")
    print ("<tr>")
    print ("<td>")
    print ("<b>Spostare messaggi \"inviati/in invio\" in \"vecchi messaggi\" ?   </b>")
    print ("</td>")
    print ("<td>")
    print (mhl.MyCheckboxForm("key","new:"+RedisKey+"*"))
    print ("</td>")
    print ("</tr>")
    print ("<tr>")
    print ("<td colspan=\"4\">")
    print ("<hr/>")
    print ("</td>")
    print ("</tr>")
    print ("<tr>")
    print ("<td>")
    print ("</td>")
    print ("<td>")
    print (mhl.MyButtonForm("submit","Submit"))
    print ("</td>")
    print ("</tr>")
    print ("</table>")
    print (mhl.MyEndForm())
    
    print ("<br>")
    print ("<br>")

Msg = (MyDB.keys("old:"+RedisKey+"*"))  # old:msg:*
Msg = sorted(Msg)
#Msg = sorted(Msg,key=lambda Msg: Msg[4], reverse=True)
if len(Msg) != 0:
    print ("<h3>Vecchi messaggi (ordinati per tipo di allarme)</h3>")
    print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
    print ("<tr>")
    print ("<td>")
    print ("<b>Key</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Date</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Type</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Description</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>Value</b>")
    print ("</td>")
    print ("<td>")
    print ("<b>u.m.</b>")
    print ("</td>")
    print ("</tr>")
    for i in range(len(Msg)):
        print ("<tr>")
        print ("<td>")
        print (Decode(Msg[i]))
        print ("</td>")
        for j in ["date", "type", "desc", "value", "um"]:
            print ("<td>")
            print (Decode(MyDB.hget(Msg[i],j)))
            print ("</td>")
        print ("</tr>")
    print ("</table>")
    
    print ("<br>")
    print ("<br>")

print (mhl.MyHtmlBottom())
