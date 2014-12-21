#!/usr/bin/env python3

## My HTML Library
#

# Html page
def MyHtml():
    return "Content-type: text/html\n\n"

def MyHtmlHead():
    return ("""
<html>

<head>
  <title>Centralino sicurezza</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="centralino, sicurezza, allarme, python">
  <meta name="Author" content="Davide">
</head>

<body>
""")

def MyHtmlBottom():
    return ("""
</body>
</html>
""")

def MyActionForm(Action,Post):
    return("<form action=\""+Action+"\" method=\""+Post+"\">")

def MyTextForm(Name,Value,Size,Required,Readonly):
    return("<input type=\"text\" name=\""+Name+"\" value=\""+Value+"\" size=\""+Size+"\" "+Required+" "+Readonly+">")

def MyMailForm(Name,Value,Size,Required,Readonly):
    return("<input type=\"email\" name=\""+Name+"\" value=\""+Value+"\" size=\""+Size+"\" "+Required+" "+Readonly+">")

def MyTextAreaForm(Name,Value,Cols,Rows,Required,Readonly):
    return("<textarea name=\""+Name+"\" value=\""+Value+"\" cols=\""+Cols+"\" rows=\""+Rows+"\" "+Required+" "+Readonly+">")

def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Required,Readonly):
    return("<input type=\"number\" name=\""+Name+"\" value=\""+Value+"\" size=\""+Size+"\" maxlenght=\""+Maxlenght+"\" min=\""+Min+"\" max=\""+Max+"\" "+Required+" "+Readonly+">")

def MyCheckboxForm(Name,Value,Required,Readonly):
    return("<input type=\"checkbox\" name=\""+Name+"\" value=\""+Value+"\" "+Required+" "+Readonly+">")

def MyRadioButton(Name,Value):
    pass	# Questa puo` avere svariati valori ... e` da pensarci su.

def MyDropDown(Name,Value):
    pass	# Questa volta value deve essere un array ... 

def MyPasswordForm(Type,Name):  # Se c'e`, e` sempre richiesta di sicuro
    return("<input type=\""+Type+"\" name=\""+Name+"\" required>")

def MyButtonForm(Type,Value):
    return("<input type=\""+Type+"\" value=\""+Value+"\">")

def MyEndForm():
    return("</form>")
