#!/usr/bin/env python3
"""
Function Library Security/Safety Unit

Libreria
Funzioni
Centralino
Sicurezza (Allarmi e Segnalazioni)

"""

import redis

def OpenDB():
    DB = redis.StrictRedis(host='localhost', port=6379, db=0, password='')
    return DB

""" Tutto il resto per ora e` inutile
def InfoDB():
    DB = OpenDB()
    return DB.info()

def GetConfigDB(Parameter):
    DB = OpenDB()
    return DB.config_get(Parameter)

## Stringhe
def WriteString(name,value):
    DB = OpenDB()
    DB.set(name,value)

def ReadString(name):
    DB = OpenDB()
    return (DB.get(name))
"""