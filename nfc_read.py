#coding: utf-8
import nfc

#wait NFC tag
clf = nfc.ContactlessFrontend('usb')		#NFCtagを受け付ける

def connected(tag):
    print tag.ndef.message.pretty() #recordの中身を表示

    for record in tag.ndef.records:
        print record.text       #recordの中のtextフィールドを表示(タイプはunicode)

clf.connect(rdwr={'on-connect':connected})	#connected()を実行
