#!/usr/bin/env python3

import mhl,redis,fls

# Servono ?
import cgi,cgitb
cgitb.enable()


# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
RedisKey = "config"

# Controllo ogni valore
if MyDB.hexists(RedisKey,"attempts"):
    Attempts = MyDB.hget(RedisKey,"attempts")
else:
    Attempts = b"1"

if MyDB.hexists(RedisKey,"delay"):
    Delay = MyDB.hget(RedisKey,"delay")
else:
    Delay = b"1"

if MyDB.hexists(RedisKey,"ttl"):
    TTL = MyDB.hget(RedisKey,"ttl")
else:
    TTL = b"1"

if MyDB.hexists(RedisKey,"tcycle"):
    TCycle = MyDB.hget(RedisKey,"tcycle")
else:
    TCycle = b"1"


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

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
print ("Nr. tentativi d'invio per messaggio: ")
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
print ("Tempo di permanenza in archivio degli avvisi (giorni): ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("ttl",TTL.decode('unicode_escape'),"3","3","1","365","required",""))
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("Tempo di funzione ciclica controllo nuovi messaggi (secondi): ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("tcycle",TCycle.decode('unicode_escape'),"2","2","1","60","required",""))
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
