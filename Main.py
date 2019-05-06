#!/usr/bin/env python3

"""

This brings together other programs to print Haikus Based on Twiiter.
You will need to input an API Key to utilise.
Thanks to Watershed in Bristol for the brilliant Idea. 
and Thanks to Hannah Satchwell for developing the idea and building the visual art for an exhibition.

Made by Callum Mulligan.

"""

import Printer
import RFID
import Twitter
import time
import sys

RFID.loadKeyword()

i = 0

while True:
    print(i)
    i = i+1
    print("Scan RFID \n")
    UID = RFID.getUID()
    Word = RFID.getRFIDKeywords(UID)
    print("Getting Tweets for:  " + Word + '\n')
    try:
        Twitter.getTweets(Word)
        Twitter.sortTweets()
        poem = Twitter.getPoem()
        print(poem[0])
        print(poem[1])
        print(poem[2])
        Printer.Message(poem)
    except Exception as e:
        print("ERROR!  ")
        print(e)
        time.sleep(2)
        continue
    time.sleep(3)