#!/bin/bash

sudo apt update -y
sudo apt install -y build-essential libdouble-conversion-dev python3-pip '^libxcb.*-dev' libx11-xcb-dev libglu1-mesa-dev libxrender-dev libxi-dev libxkbcommon-dev libxkbcommon-x11-dev blueman
sudo pip install bsp-eog-1.0.1.tar.gz
