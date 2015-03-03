#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()

# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Redis "key"
RedisKey = "list:mail"


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

form=cgi.FieldStorage()

if "rpush" in form:
    MyDB.rpush(RedisKey, cgi.escape(form["rpush"].value))
if "lrem" in form:
    MyDB.lrem(RedisKey, 0, cgi.escape(form["lrem"].value))
    # Ho deciso di eliminare tutte le occorrenze
    # In realta` il comando avrebbe molte piu` possibilita`.

print ("<h2>Dati inseriti/modificati:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
print ("<tr>")
print ("<td>")
print (RedisKey)
print ("</td>")
print ("<td>")
print (MyDB.lrange(RedisKey,0,-1))
print ("</td>")
print ("</tr>")
print ("</table>")

print (mhl.MyHtmlBottom())
