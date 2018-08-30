import nfc

import RPi.GPIO as GPIO
import time

PIN = [25,24,23,22,21,20]               #ラズパイのGPIOピンの番号
GPIO.setmode(GPIO.BCM)                  #BCMモードのピンアサインを使用
GPIO.setup(PIN,GPIO.OUT)

#wait NFC tag
clf = nfc.ContactlessFrontend('usb')

def outputting():
    GPIO.output(PIN,(False,False,True,False,False,False))   #ここでどのピンに電流流すか決めてる(Trueで電流流す)
                                                            #左から25,24,...,20になっている
    if GPIO.input(25):
        text = "a"
    elif GPIO.input(24):
        text = "b"
    elif GPIO.input(23):
        text = "c"
    elif GPIO.input(22):
        text = "d"
    elif GPIO.input(21):
        text = "e"
    elif GPIO.input(20):
        text = "f"
    else:
        print "can't searching PIN"
        text = "error"

    print "%s is writing" % text

    GPIO.output(PIN,False)                                  #電流止める

    return text

def connected(tag):
    print tag.ndef.message.pretty()

    adding = outputting()

    if tag.ndef.records:                                    #2回目以降
        for record in tag.ndef.records:
            print record.text                               #recordの中のtextフィールドを表示(タイプはunicode)
            nfc_tx = record.text.encode()                   #unicode -> str
#            print type(nfc_tx)  デバッグ用
            nfc_write_tx = nfc_tx + adding
#            print "%s type= %s" % (nfc_write_tx,type(nfc_write_tx))  デバッグ用
            record = nfc.ndef.TextRecord(nfc_write_tx)      #書き込むデータを指定
            tag.ndef.message = nfc.ndef.Message(record)     #指定したデータを書き込み
            print tag.ndef.message.pretty()                 #書き込んだデータを含んだレコード全体を表示
    else:                                                   #初回書き込みの時
        record = nfc.ndef.TextRecord(adding)
        tag.ndef.message = nfc.ndef.Message(record)
        print tag.ndef.message.pretty()


clf.connect(rdwr={'on-connect':connected})
GPIO.cleanup()                                              #全てのピンを解除
