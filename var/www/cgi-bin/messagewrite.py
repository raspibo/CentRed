#!/usr/bin/env python3

import mhl,redis,fls,time

# Servono ?
import cgi,cgitb
cgitb.enable()

# Apro il database Redis con l'istruzione della mia libreria
MyDB = fls.OpenDB()

# Account Redis "key"
RedisKey = "msg"


# Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())


form=cgi.FieldStorage()

if "key" in form:
    for i in range(len(MyDB.keys(cgi.escape(form["key"].value)+"*"))):
        OldKey = (MyDB.keys(cgi.escape(form["key"].value)+"*")[i-1]).decode('unicode_escape')   # il -1 !!! ricordati
        # il [4:] serve per eliminare il new:
        NewKey = ("old:"+OldKey[4:]+":"+time.strftime("%Y%m%d%H%M%S", time.localtime()))
        print ("<b>Renamed</b> ", OldKey," <b>to</b> ",NewKey,"\n")
        #print (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
        MyDB.rename(OldKey,NewKey)
        #MyDB.expire(NewKey,3600)        # Per ora metto un'ora, perche` sto` facendo le prove
        #MyDB.expire(NewKey,86400)      # 24 ore
        MyDB.expire(NewKey,86400*MyDB.hget("config","ttl"))    # 24h (1g) * TTL in configurazione
else:
    print("Nessuna modifica ..")


print (mhl.MyHtmlBottom())
