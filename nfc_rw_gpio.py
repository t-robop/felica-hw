import nfc

import RPi.GPIO as GPIO
import time
import sys
import signal

PIN = [26,25,24,23,22,21,20,19,18]     #25~20PIN is for tag, 26,19,18,17PIN is for LED

def outputting():
    GPIO.output(PIN,(False,True,True,True,True,True,True,False,False,False))    #25~20PIN flow A

    if GPIO.input(25) == 0:
        text = "a"
        GPIO.output(18,True)        #Lighting LED
    elif GPIO.input(24) == 0:
        text = "b"
        GPIO.output(18,True)        #Lighting LED
    elif GPIO.input(23) == 0:
        text = "c"
        GPIO.output(18,True)        #Lighting LED
    elif GPIO.input(22) == 0:
        text = "d"
        GPIO.output(18,True)        #Lighting LED
    elif GPIO.input(21) == 0:
        text = "e"
        GPIO.output(18,True)        #Lighting LED
    elif GPIO.input(20) == 0:
        text = "f"
        GPIO.output(18,True)        #Lighting LED
    else:
        print "can't searching PIN"
        text = "error"

    print "%s is writing" % text    #display writing data
    return text

def connected(tag):
    print tag.ndef.message.pretty() #display ntag's record

    adding = outputting()

    if tag.ndef.records:            #after 2 counts
        for record in tag.ndef.records:
            print record.text       #display ntag data
            nfc_tx = record.text.encode()
#Debug            print type(nfc_tx)
            nfc_write_tx = nfc_tx + adding
#Debug            print "%s type= %s" % (nfc_write_tx,type(nfc_write_tx))
            if nfc_write_tx.find("error") >= 0: #return error
                print "Error: return exception"
                GPIO.output(18,False)       #power off LED
                GPIO.output(19,True)        #Lighting Error LED
            else:
                if len(set(list(nfc_write_tx))) == len(nfc_write_tx):   #not duplicate
                    record = nfc.ndef.TextRecord(nfc_write_tx)
                    tag.ndef.message = nfc.ndef.Message(record)         #write data to ntag
                    print tag.ndef.message.pretty()
                else:
                    print "Error: Text data duplicate!!"
                    GPIO.output(18,False)   #power off LED
                    GPIO.output(17,True)    #Lighting Error LED
    else:
        if adding.find("error") >= 0:
            print "Error: return exception"
            GPIO.output(18,False)           #power off LED
            GPIO.output(19,True)            #Lighting Error LED
        else:
            record = nfc.ndef.TextRecord(adding)
            tag.ndef.message = nfc.ndef.Message(record)
            print tag.ndef.message.pretty()

    time.sleep(2)
    GPIO.output(PIN,False)

try:
    while 1:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(PIN,GPIO.OUT)
        GPIO.output(26,True)
        time.sleep(1)
        GPIO.output(26,False)
        #wait NFC tag
        print "nfc tag connected...."
        clf = nfc.ContactlessFrontend('usb')
        clf.connect(rdwr={'on-connect':connected})
        GPIO.cleanup()              #release GPIO
        clf.close()                 #close nfc connection
except:
    GPIO.output(19,True)
    time.sleep(1)
    GPIO.output(19,False)      
    GPIO.cleanup()
    clf.close()
    print "prog is finish!"
    sys.exit(0)
