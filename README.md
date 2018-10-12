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

