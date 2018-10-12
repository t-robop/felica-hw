# felica-hw

## Description
TAPで使うライタ側の制御プログラム
リーダライタにかざしたntagに対してピンで指定したブース番号を書き込む

## Requirement
### Python version
v3.7.x

### Operating System
- Raspbian OS

## Setup
### Mac(debug)
``` bash
sudo pip install -U nfcpy
```
``` bash
git clone https://github.com/t-robop/felica-hw
```
``` bash
cd felica-hw
python3 nfc_rw_gpio.py 
```

### Linux(Register to systemd)
``` bash
sudo pip install -U nfcpy
git clone https://github.com/t-robop/felica-hw
```
```bash
sudo vi /lib/systemd/system/nfc.service
```
```　:/lib/systemd/system/nfc.service
[Unit]
Description=NFC Writer service
Requires=dev-pasori320.device
After=dev-pasori320.device

[Service]
Type=simple
ExecStart=/bin/sh -c "echo Hello by `date` >> /home/pi/hello2.log"

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable nfc.service
sudo systemctl --system daemon-reload
sudo systemctl status nfc.service
```


## How to use
- RaspbierryPiにPaSoRiを接続した状態で起動。
- PaSoRiが接続され立ち上がれば緑LEDが点灯
- 

## LED Status

| LED | Status | Detailes |
|:----------:|:-----------:|:------------:|
| Green | Ready | 書き込める状態 |
| RGBLED's Green Flashing | Writing | 書き込み中 |
| RGBLED's Red Flashing | Writing error | 書き込みエラー
| RGBLED's Red && Red | Other error | その他のエラー、深刻 |
| No LEDs | Not started | そもそもスクリプトが動いてない状態、やばい |

## License
MIT


# how to
tagかざす -> ピンごとに書き込むデータを決める -> tagのテキスト読み取ってそれに書き込むデータを追加する -> 上手にできました 

# 使用機材
- Raspberry Pi 3 Model B 1個
- Pasori RC-S380 1個
- LED 7個(フルカラーLED1個で検討中)
- ブレッドボード 1個
- ジャンパー線

## Python Version
- v2.7

# 仕様
## 概要
- 現在はラズパイの電源を入れたらnfcのプログラムが実行される。
- ~~書き込みが成功した時と失敗した時で光るLEDを変えている。(フルカラーLEDで検討中)~~
- フルカラーLED : 赤色・・・書き込み成功、 青色・・・文字が重複するためエラー、 緑色・・・プログラム開始の合図
- 単色赤・・・文字重複時以外のエラー発生時に点灯
- 書き込む文字はブースごと１文字(s,t,u,vのどれか)

## 自動実行について
- ラズパイに`systemctl enable test.service`を指定することで自動実行
- test.serviceにはこのように記述してある

```txt:test.service
[Unit]
Description = Test

[Service]
ExecStart=/usr/bin/python3 /home/pi/hogehoge(自動実行したいプログラムのルート,この場合はhogehogeが設定される)
Restart=always
Type=simple

[Install]
WantedBy=multi-user.target
```

Serviceに関してはudevとからめたunitの制御をしてあげないとうまく動かない。要確認。
http://thinkami.hatenablog.com/entry/2015/06/25/064658

### 設定方法
- 1 `sudo vi /lib/systemd/system/nfc.service`
- 2 上記test.serviceを参考に設定を書く
- 3 `sudo systemctl enable nfc.service`
