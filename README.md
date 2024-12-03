# Instrucciones de Instalación

```sh
python3.11 -m venv ./.venv
source ./.venv/bin/activate
pip install -r requirements.txt
pip install --upgrade pip
python setup.py develop
juopyter lab
```

## Conectar Bluetooth en Linux

```sh
bluetoothctl

[bluetooth]# power on
Changing power on succeeded

[bluetooth]# agent on
Agent registered

[bluetooth]# default-agent
Default agent request successfull

[bluetooth]# scan on
...
[bluetooth]# scan off
Discovery stopped

[bluetooth]# pair 98:D3:51:FD:9D:70
Enter PIN code: 1234
Pairing successfull
```
