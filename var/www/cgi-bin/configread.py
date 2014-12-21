#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
RedisKey = "config"

if MyDB.hlen(RedisKey) == 0:
    Attempts = b"1"
    Delay = b"1"
    TTL = b"1"
else:
    Attempts = MyDB.hget(RedisKey,"attempts")
    Delay = MyDB.hget(RedisKey,"delay")
    TTL = MyDB.hget(RedisKey,"ttl")


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())


print (mhl.MyActionForm("/cgi-bin/configwrite.py","POST"))

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
print ("Nr. tentativi d'invio: ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("attempts",Attempts.decode('unicode_escape'),"3","3","1","100","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Tempo d'intervallo fra tentativi (minuti): ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("delay",Delay.decode('unicode_escape'),"3","3","1","120","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Tempo di sopravvivenza in archivio degli avvisi (giorni): ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("ttl",TTL.decode('unicode_escape'),"3","3","1","365","required",""))
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
