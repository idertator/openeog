#!/bin/bash

VERSION=1.0.2

sudo apt update -y
sudo apt install -y build-essential libdouble-conversion-dev python3-pip '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev blueman setserial
sudo pip install bsp-eog-$VERSION.tar.gz
sudo usermod -a -G tty $USER
sudo usermod -a -G dialout $USER
sudo usermod -a -G plugdev $USER
sudo usermod -a -G netdev $USER
sudo usermod -a -G bluetooth $USER
