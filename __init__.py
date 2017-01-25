# -*- coding: latin1 -*-

from main import checkFeicao    


def name():
  return "check feições"
def description():
  return "mostra cada uma das feições da camada ativa"
def version():
  return "Version 0.1"

def classFactory(iface):
  from main import checkFeicao
  return checkFeicao(iface)

def qgisMinimumVersion():
  return "2.0"
def author():
  return "sam"
def email():
  return "me@hotmail.com"
def icon():
  return "next.png", "back.png"

## any other initialisation needed
