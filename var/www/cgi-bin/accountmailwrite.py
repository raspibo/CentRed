#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()

# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())


form=cgi.FieldStorage()

Errore=0
for i in ["key", "username", "password", "mailfrom", "serversmtp", "port"]:
    if i not in form:
        Errore = Errore+1
        print ("Manca il valore:",i)

if Errore == 0:
    MyDB.hmset("account:mail", {"username":cgi.escape(form["username"].value), "password":cgi.escape(form["password"].value), "mailfrom":cgi.escape(form["mailfrom"].value), "serversmtp":cgi.escape(form["serversmtp"].value), "port":cgi.escape(form["port"].value)})

print ("<h2>Dati inseriti:</h2>")
print ("<br>")
print (MyDB.hgetall("account:mail"))

print (mhl.MyEndForm())
