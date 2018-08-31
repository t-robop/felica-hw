import nfc

import RPi.GPIO as GPIO
import time

PIN = [25,24,23,22,21,20,19,18]     #25~20PIN is for tag, 19,18PIN is for LED
GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN,GPIO.OUT)

#wait NFC tag
clf = nfc.ContactlessFrontend('usb')

def outputting():
    GPIO.output(PIN,(True,True,True,True,True,True,False,False))    #25~20PIN flow A

    if GPIO.input(25) == 0:
        text = "a"
        GPIO.output(19,True)        #Lighting LED
    elif GPIO.input(24) == 0:
        text = "b"
        GPIO.output(18,True)        #Lighting LED
    elif GPIO.input(23) == 0:
        text = "c"
    elif GPIO.input(22) == 0:
        text = "d"
    elif GPIO.input(21) == 0:
        text = "e"
    elif GPIO.input(20) == 0:
        text = "f"
        GPIO.output(19,True)        #Lighting LED
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
#            print type(nfc_tx)     *for debug*
            nfc_write_tx = nfc_tx + adding
#            print "%s type= %s" % (nfc_write_tx,type(nfc_write_tx))    *for debug*
            if nfc_write_tx.find("error") >= 0:     #return error
                print "Error: return exception"
            else:
                if len(set(list(nfc_write_tx))) == len(nfc_write_tx):   #not duplicate
                    record = nfc.ndef.TextRecord(nfc_write_tx)
                    tag.ndef.message = nfc.ndef.Message(record)         #write data to ntag
                    print tag.ndef.message.pretty()
                else:
                    print "Error: Text data duplicate!!"
    else:
        if adding.find("error") >= 0:
            print "Error: return exception"
        else:
            record = nfc.ndef.TextRecord(adding)
            tag.ndef.message = nfc.ndef.Message(record)
            print tag.ndef.message.pretty()

    time.sleep(2)
    GPIO.output(PIN,False)


clf.connect(rdwr={'on-connect':connected})
GPIO.cleanup()      #release GPIO
