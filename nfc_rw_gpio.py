import nfc

import RPi.GPIO as GPIO
import time
import sys
import signal

PIN = [26, 25, 24, 23, 22, 19, 18]  # 25~20PIN is for tag, 26,19,18,17PIN is for LED

# 書き込み文字判別用
WRITE_PIN_S = 26
WRITE_PIN_T = 19
WRITE_PIN_U = 13
WRITE_PIN_V = 6

# フルカラーLED用
F_LED_R = 17
F_LED_G = 27
F_LED_B = 22

# 赤色LED用
R_LED = 18

# enum用定数
ENUM_WRITE_OK = 1
ENUM_WRITING = 2
ENUM_WRITE_DONE = 3
ENUM_WRITE_ERROR = 4
ENUM_SYS_ERROR = 5

'''
# 全体的な流れ
1. gpioを読み込んで書き込む文字を決める(これはループしない)
2. LED発光用メソッドを作る
    これはenumで、エラー、書き込み中、書き込みOKを作ってわたしてあげる感じかな
3. nfcの値をリードする、自分が書き込む文字列がかいてあったら書き込まずにLEDを光らせて終了する
4. 書き込む値が違ったら書き込む(この時LEDは点滅させる)
5. 書き込み終わったら再度Readして、同じ文字があるか確認する
6. 同じ文字があったら書き込み終了と判断する

7. system系でエラーが有った時(デバイスないとか)は全部のLEDをあかにする


# LED発光の詳細
1. 緑点灯は書き込みできる
2. フルカラーの赤点滅は書き込みエラー
3. どちらも赤はその他のエラー
4. 書き込み中は緑点滅
'''


def led_start(state):
    if state == ENUM_WRITE_OK:
        print("書き込みOK")
        GPIO.output(F_LED_G, True)
        GPIO.output(F_LED_R, False)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, False)

    elif state == ENUM_WRITING:
        print("書き込み中")
        GPIO.output(F_LED_G, True)
        GPIO.output(F_LED_R, False)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, False)
        time.sleep(0.2)
        GPIO.output(F_LED_G, False)
        GPIO.output(F_LED_R, False)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, False)
        time.sleep(0.2)

    elif state == ENUM_WRITE_DONE:
        print("書き込み終了")
        GPIO.output(F_LED_G, False)
        GPIO.output(F_LED_R, False)
        GPIO.output(F_LED_B, True)
        GPIO.output(R_LED, False)
        time.sleep(1.5)

    elif state == ENUM_WRITE_ERROR:
        print("書き込み失敗")
        GPIO.output(F_LED_G, False)
        GPIO.output(F_LED_R, True)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, False)
        time.sleep(0.2)
        GPIO.output(F_LED_G, False)
        GPIO.output(F_LED_R, False)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, False)
        time.sleep(0.2)

    elif state == ENUM_WRITE_ERROR:
        print("致命的なエラー")
        GPIO.output(F_LED_G, False)
        GPIO.output(F_LED_R, True)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, True)


def outputting():
    GPIO.output(PIN, (False, True, True, True, True, False, False, False))  # 25~20PIN flow A

    if GPIO.input(25) == 0:
        text = "s"
        GPIO.output(18, True)  # Lighting LED
    elif GPIO.input(24) == 0:
        text = "t"
        GPIO.output(18, True)  # Lighting LED
    elif GPIO.input(23) == 0:
        text = "u"
        GPIO.output(18, True)  # Lighting LED
    elif GPIO.input(22) == 0:
        text = "v"
        GPIO.output(18, True)  # Lighting LED
    else:
        print "can't searching PIN"
        text = "error"

    print "%s is writing" % text  # display writing data
    return text


def connected(tag):
    print tag.ndef.message.pretty()  # display ntag's record

    adding = outputting()

    if tag.ndef.records:  # after 2 counts
        for record in tag.ndef.records:
            print record.text  # display ntag data
            nfc_tx = record.text.encode()
            # Debug            print type(nfc_tx)

            # Debug            print "%s type= %s" % (nfc_write_tx,type(nfc_write_tx))
            if adding == "error":  # return error
                print "Error: return exception"
                GPIO.output(18, False)  # power off LED
                GPIO.output(19, True)  # Lighting Error LED
            else:
                if nfc_tx.find(adding) == -1:  # not duplicate
                    nfc_write_tx = nfc_tx + adding
                    record = nfc.ndef.TextRecord(nfc_write_tx)
                    tag.ndef.message = nfc.ndef.Message(record)  # write data to ntag
                    print tag.ndef.message.pretty()
                else:
                    print "Error: Text data duplicate!!"
                    GPIO.output(18, False)  # power off LED
                    GPIO.output(17, True)  # Lighting Error LED
    else:
        if adding.find("error") >= 0:
            print "Error: return exception"
            GPIO.output(18, False)  # power off LED
            GPIO.output(19, True)  # Lighting Error LED
        else:
            record = nfc.ndef.TextRecord(adding)
            tag.ndef.message = nfc.ndef.Message(record)
            print tag.ndef.message.pretty()

    time.sleep(2)
    GPIO.output(PIN, False)


while True:
    led_start(ENUM_WRITE_OK)
    # time.sleep(2)
    # GPIO.output(11, False)
    # time.sleep(2)

#
# try:
#     while 1:
#         GPIO.setmode(GPIO.BCM)
#         GPIO.setup(PIN, GPIO.OUT)
#         GPIO.output(26, True)
#         time.sleep(1)
#         GPIO.output(26, False)
#         # wait NFC tag
#         print "nfc tag connected...."
#         clf = nfc.ContactlessFrontend('usb')
#         clf.connect(rdwr={'on-connect': connected})
#         GPIO.cleanup()  # release GPIO
#         clf.close()  # close nfc connection
# except:
#     GPIO.output(19, True)
#     time.sleep(1)
#     GPIO.output(19, False)
#     GPIO.cleanup()
#     clf.close()
#     print "prog is finish!"
#     sys.exit(0)
