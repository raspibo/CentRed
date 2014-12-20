#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
Account = "account:xmpp"

if MyDB.hlen(Account) == 0:
    Username = b"vuoto"
    #Password = b"vuota"
else:
    Username = MyDB.hget(Account,"username")
    #Password = MyDB.hget(Account,"password")

# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())


print (mhl.MyActionForm("/cgi-bin/accountxmppwrite.py","POST"))

print ("<table>")

print ("<tr>")
print ("<td>")
print ("Key: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("key",Account,"40","required","readonly"))
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
print ("<td colspan=\"2\">")
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
