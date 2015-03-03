#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
RedisKey = "account:mail"

if MyDB.hlen(RedisKey) == 0:
    Username = b"vuoto"
    #Password = b"vuota"
    Mailfrom = b"vuota"
    ServerSMTP = b"vuoto"
    Port = b"0"
else:
    Username = MyDB.hget(RedisKey,"username")
    #Password = MyDB.hget(RedisKey,"password")
    Mailfrom = MyDB.hget(RedisKey,"mailfrom")
    ServerSMTP = MyDB.hget(RedisKey,"serversmtp")
    Port = MyDB.hget(RedisKey,"port")


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

print (mhl.MyActionForm("/cgi-bin/accountmailwrite.py","POST"))

print ("<table>")

print ("<tr>")
print ("<td>")
print ("Key: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("key",RedisKey,"40","required","readonly"))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Username: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("username",Username.decode('unicode_escape'),"40","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Password: ")
print ("</td>")
print ("<td>")
print (mhl.MyPasswordForm("password","password"))
#print (mhl.MyTextForm("password",Password.decode('unicode_escape'),"40","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Mail from: ")
print ("</td>")
print ("<td>")
print (mhl.MyMailForm("mailfrom",Mailfrom.decode('unicode_escape'),"40","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Server: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("serversmtp",ServerSMTP.decode('unicode_escape'),"40","required",""))
print ("</td>")
print ("<td>")
print ("port: ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("port",Port.decode('unicode_escape'),"6","6","0","32767","required",""))
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
