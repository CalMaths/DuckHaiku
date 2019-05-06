#!/usr/bin/env python

"""

By Callum Mulligan

A simple module to print a Haiku to a recipt printer.
Utlises the wonderful escpos library

https://pypi.org/project/python-escpos/

"""

from escpos import *
from time import sleep

RPrinter = printer.File("/dev/usb/lp0")

RPrinter.set(
        font='a',
        height=1,
        align='center',
        )

def Break():
    RPrinter.text("\n\n\n")

def Message(poem):
    Break()
    RPrinter.text("    __  \n___( o)>\n \ <_. ) \n `---'   ")
    RPrinter.text("\nHook-a-Haiku duck says:\n")
    RPrinter.text("\n-----------------------\n")
    for line in poem:
        RPrinter.text(line + "\n")
    RPrinter.text("\n-----------------------\n")
    RPrinter.text("      _      _      _        \n>(.)__ <(.)__ =(.)__\n (___/  (___/  (___/")        
    Break()
    RPrinter.text("This project was created by Hannah Satchwell and Callum Mulligan ( http://www.callummulligan.co.uk ) to exhibit at the Young Producers takeover event. Find us on social media!")
    Break()

if __name__ == '__main__':
    Message(["I am a Duck"," A Mighty Duck", "Yes A Duck.... Quack."])
    