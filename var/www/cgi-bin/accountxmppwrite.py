#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()

# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
RedisKey = "account:xmpp"


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

form=cgi.FieldStorage()

for i in ["username", "password"]:
    if i not in form:
        print ("<h3>Manca il valore: </h3>",i)
    else:
        MyDB.hset(RedisKey,i,cgi.escape(form[i].value))

print ("<h2>Dati inseriti/modificati:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
print ("<tr>")
print ("<td>")
print (RedisKey)
print ("</td>")
print ("<td>")
print (MyDB.hgetall(RedisKey))
print ("</td>")
print ("</tr>")
print ("</table>")

print (mhl.MyHtmlBottom())
