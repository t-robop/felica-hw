import nfc
clf = nfc.ContactlessFrontend('usb')			#NFCtagがかざされるのを待つ
  
def connected(tag)
    record = nfc.ndef.TextRecord("Hello World!")	#書き込むデータを指定
    tag.ndef.message = nfc.ndef.Message(record)		#指定したデータを書き込み
    print tag.ndef.message.pretty()			#書き込んだデータを含んだレコード全体を表示
  
clf.connect(rdwr={'on-connect': connected})		#connected()を実行

