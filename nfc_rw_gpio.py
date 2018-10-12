# coding:utf-8

import nfc

import RPi.GPIO as GPIO
import time
import sys
import signal

PIN = [26, 19, 13, 6, 17, 27, 22, 18]  # 25~20PIN is for tag, 26,19,18,17PIN is for LED

# 書き込み文字判別用
WRITE_PIN_S = 26
WRITE_PIN_T = 19
WRITE_PIN_U = 13
WRITE_PIN_V = 6

# フルカラーLED用
F_LED_R = 17
F_LED_G = 22
F_LED_B = 27

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

    elif state == ENUM_SYS_ERROR:
        print("致命的なエラー")
        GPIO.output(F_LED_G, False)
        GPIO.output(F_LED_R, True)
        GPIO.output(F_LED_B, False)
        GPIO.output(R_LED, True)


def output_str_select():
    if GPIO.input(WRITE_PIN_S) == 0:
        text = "s"

    elif GPIO.input(WRITE_PIN_T) == 0:
        text = "t"

    elif GPIO.input(WRITE_PIN_U) == 0:
        text = "u"

    elif GPIO.input(WRITE_PIN_V) == 0:
        text = "v"

    else:
        print "can't searching PIN"
        text = "error"

    print "%s is writing" % text  # display writing data
    return text


def nfc_read(tag):
    str = tag.ndef.message.pretty()
    print(str)
    return str


def nfc_write(tag, write_str):
    tag.ndef.message = nfc.ndef.Message(write_str)


def connected(tag):
    led_start(ENUM_WRITING)
    nfc_text = nfc_read
    if G_output_text in nfc_text:
        print("すでに書き込まれています")
        led_start(ENUM_WRITE_DONE)
        return

    nfc_write(G_output_text)

    nfc_text = nfc_read
    if G_output_text in nfc_text:
        print("書き込み成功")
        led_start(ENUM_WRITE_DONE)
        return
    else:
        print("書き込み失敗")
        led_start(ENUM_WRITE_ERROR)
        return



GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)
G_output_text = output_str_select

if "error" in G_output_text:
    led_start(ENUM_SYS_ERROR)
    sys.exit(1)

while True:
    clf = nfc.ContactlessFrontend('usb')
    clf.connect(rdwr={'on-connect': connected})
    clf.close()
