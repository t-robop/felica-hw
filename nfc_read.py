import nfc

#wait NFC tag
clf = nfc.ContactlessFrontend('usb')

def connected(tag):
    print tag.ndef.message.pretty() #detail record

    for record in tag.ndef.records:
        print record.text       #type is unicode 

clf.connect(rdwr={'on-connect':connected})
