#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Redis "key"A
RedisKey = "alarm:list"


if MyDB.llen(RedisKey) == 0:
    Lists = ''
else:
    Lists = MyDB.lrange(RedisKey,0,-1)

# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

print ("<h3>Selezione delle liste di invio messaggi di allarme</h3>")
print ("Possono essere aggiunte/eliminate contemporaneamente, ma una sola lista alla volta")
print ("<br>")
print ("<br>")

print (mhl.MyActionForm("/cgi-bin/alarmlistwrite.py","POST"))

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
print ("Aggiungi lista: ")
print ("</td>")
print ("<td>")
#print (mhl.MyTextForm("rpush","","40","",""))
Keys = MyDB.keys("list*")
print ("<select name=\"rpush\">")
print ("<option value=\"""\"> </option>")
for i in range(len(Keys)):
    KeyValue = Keys[i-1].decode('unicode_escape')
    print ("<option value=\""+KeyValue+"\">"+KeyValue+"</option>")
print ("</select>")

print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Elimina lista: ")
print ("</td>")
print ("<td>")
#print (mhl.MyTextForm("lrem","","40","",""))
Keys = MyDB.keys("list*")
print ("<select name=\"lrem\">")
print ("<option value=\"""\"> </option>")
for i in range(len(Keys)):
    KeyValue = Keys[i-1].decode('unicode_escape')
    print ("<option value=\""+KeyValue+"\">"+KeyValue+"</option>")
print ("</select>")

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
