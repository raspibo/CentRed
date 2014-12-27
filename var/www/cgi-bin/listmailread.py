#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Redis "key"A
RedisKey = "list:mail"


if MyDB.llen(RedisKey) == 0:
    Lists = ''
else:
    Lists = MyDB.lrange(RedisKey,0,-1)

# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())

print ("<h3>Puoi aggiungerne o eliminarne solamente uno alla volta</h3>")
print ("(Anche contemporaneamente, ma un'indirizzo solo)")
print ("<br>")
print ("<br>")

print (mhl.MyActionForm("/cgi-bin/listmailwrite.py","POST"))

print ("<table>")

print ("<tr>")
print ("<td>")
print ("Key: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("key",RedisKey,"40","required","readonly"))
print ("</td>")
print ("</tr>")

for i in range(len(Lists)):
    print ("<tr>")
    print ("<td>")
    print ("Value: ")
    print ("</td>")
    print ("<td>")
    print (mhl.MyTextForm("lists",Lists[i].decode('unicode_escape'),"40","required","readonly"))
    print ("</td>")
    print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Aggiungi: ")
print ("</td>")
print ("<td>")
print (mhl.MyMailForm("rpush","","40","",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Elimina: ")
print ("</td>")
print ("<td>")
print (mhl.MyMailForm("lrem","","40","",""))
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
print (mhl.MyHtmlBottom())
