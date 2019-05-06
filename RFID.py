#!/usr/bin/env python3

"""

Adapted from: https://github.com/tsndr/MFRC522-python
Utilises: https://github.com/pimylifeup/MFRC522-python

By Callum Mulligan.

NoAuthRead/NoAuthWrite was an attempt to enable read/writing to NFC NTAG213 tags. 

While I was along the right lines and with more time cetainly would have come to a solution I instead took the ID of the Tags and saved the information
in the program.

When run this will save a file of keywords associated with tag ID's

"""

import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
import mfrc522 
import signal

continue_reading = True

RFIDKeywords = {
    
}

def noAuthRead():
 
    def format_uid(uid):
        s = ""
        for i in range(0, len(uid)):
            s += "%x" % uid[i]
        return s.upper()

    RFID = mfrc522.MFRC522()

    (Status, TagSize) = RFID.MFRC522_Request(RFID.PICC_REQIDL)

    while True:

        if TagSize > 0:
            message = "Sector [1 - %s]: " % (TagSize - 1)
        else:
            message = "Sector: "

        try:
            Sector = 2
        except:
            print ("")
            break
        else:
            print ("Waiting for Tag...\n")

        while True:

            (Status, TagSize) = RFID.MFRC522_Request(RFID.PICC_REQIDL)
        
            if Status != RFID.MI_OK:
                continue

            if TagSize < 1:
                print("Can't read tag properly!")
                break

            if Sector < 1 or Sector > (TagSize - 1):
                print ("Sector out of range (1 - %s)\n" % (TagSize - 1))
                break

            # Selecting blocks
            BaseBlockLength = 4
            if Sector < 32:
                BlockLength = BaseBlockLength
                StartAddr = Sector * BlockLength
            else:
                BlockLength = 16
                StartAddr = 32 * BaseBlockLength + (Sector - 32) * BlockLength

            BlockAddrs = []
            for i in range(0, (BlockLength - 1)):
                BlockAddrs.append((StartAddr + i))
            TrailerBlockAddr = (StartAddr + (BlockLength - 1))

            # Initializing tag
            (Status, UID) = RFID.MFRC522_Anticoll()

            if Status != RFID.MI_OK:
                break

            # Reading sector
            RFID.MFRC522_SelectTag(UID)
            #Status = RFID.MFRC522_Auth(RFID.PICC_AUTHENT1A, TrailerBlockAddr, KEY, UID)
            data = []
            text_read = ""
            
            for block_num in BlockAddrs:
            #for block_num in range(4,45):    
                
                block = RFID.MFRC522_Read(block_num) 
                print(block_num, " : ", block)
                if block :
                    data += block
            if data:
                text_read = "".join(chr(i) for i in data)
                #text_read = format_uid(data)
            print ("UID:  ", format_uid(UID), "   |   ",UID)
            print ("Data: ", text_read,"\n")
            
            RFID.MFRC522_StopCrypto1()
            break

    RFID.AntennaOff()
    GPIO.cleanup()

def AuthWrite(Data):
    print("Setting Up RFID Reader")
    reader = SimpleMFRC522()
    try:
        print("Now place your tag to write")
        reader.write(Data)
        print("Written:  " + str(Data))
    finally:
        GPIO.cleanup()

def AuthRead():
    print("Setting Up RFID Reader")
    reader = SimpleMFRC522()
    try:
            print("Present RFID")
            id, text = reader.read()
            print(id)
            print(text)
            return id,text
    finally:
            GPIO.cleanup()

def getUID():
    def format_uid(uid):
            s = ""
            for i in range(0, len(uid)):
                s += "%x" % uid[i]
            return s.upper()

    print("Awaiting Card")

    RFID = mfrc522.MFRC522()
    
    while True:
        (Status, TagSize) = RFID.MFRC522_Request(RFID.PICC_REQIDL)
        if Status is 0:
            (Status, UID) = RFID.MFRC522_Anticoll()
            print(format_uid(UID))
            return format_uid(UID)
        #print(Status,"  :  ", TagSize)
    RFID.MFRC522_StopCrypto1()
    RFID.AntennaOff()
    GPIO.cleanup()

def getRFIDKeywords(ID):
    return RFIDKeywords[ID]

def setRFIDKeywords(word):
    UID = getUID()
    RFIDKeywords[UID] = word
    filename = "RFIDKeywordMap.txt"
    file = open(filename, "a")
    file.write(UID + " " + word)
    file.write("\n")
    file.close()

def loadKeyword():
    filename = "RFIDKeywordMap.txt"
    file = open(filename, "r")
    for line in file:
        load = line.split(',')
        d = {}
        for l in load:
            (key, val) = l.split(' ')
            RFIDKeywords[key.strip()] = val.strip()

    print (RFIDKeywords)



if __name__ == '__main__':
    import sys
    print (sys.argv)
    while True:
        setRFIDKeywords(input("Please enter the keyword:   "))