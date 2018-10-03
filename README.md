# felica-hw
TAPで使うハードウェアの制御プログラム

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
- 書き込みが成功した時と失敗した時で光るLEDを変えている。(フルカラーLEDで検討中)

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


