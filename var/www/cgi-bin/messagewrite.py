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
print (mhl.MyHtmlHead())

form=cgi.FieldStorage()

if "key" in form:
    for i in range(len(MyDB.keys(cgi.escape(form["key"].value)+"*"))):
        # Non capisco l'indice, sembra che cambi ... 
        OldKey = (MyDB.keys(cgi.escape(form["key"].value)+"*")[0]).decode('unicode_escape')
        # il [4:] serve per eliminare il new:
        #NewKey = ("old:"+OldKey[4:]+":"+time.strftime("%Y%m%d%H%M%S", time.localtime()))
        NewKey = ("old:"+OldKey[4:])
        print ("<b>Renamed</b> ", OldKey," <b>to</b> ",NewKey,"<br>")
        #print (time.strftime("%Y/%m/%d %H:%M:%S", time.localtime()))
        MyDB.rename(OldKey,NewKey)
        #MyDB.expire(NewKey,3600)        # Per ora metto un'ora, perche` sto` facendo le prove
        #MyDB.expire(NewKey,86400)      # 24 ore
        MyDB.expire(NewKey,86400 * int(MyDB.hget("config","ttl").decode('unicode_escape')))    # 24h (1g) * TTL in configurazione
else:
    print("Nessuna modifica ..")


print (mhl.MyHtmlBottom())
