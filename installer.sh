#!/usr/bin/env bash

## README
# if any version of pip currently installed is borked, please use this guide to downgrade pip
# please NOTE, this does not sync with pacman, as this is a manual installation (https://pip.pypa.io/en/stable/installing/)

# as of writing this, version 19.03 is broken with a weird import bug
# please use this command to restore to pip version 18.02, which is known to work with Python 3.8

# $ curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
# python get-pip.py pip==18

pacman -Sy --noconfirm python-pip
pip3 install awsebcli --upgrade

if [[ -f "$HOME/.bashrc" ]]; then
        CONFIG_FILE="$HOME/.bashrc"
else
        CONFIG_FILE="$HOME/.zshrc"
fi

LOCAL_PATH="$HOME/.local/bin/"
echo "export PATH=$LOCAL_PATH:$PATH" >> $CONFIG_FILE
