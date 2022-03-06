#!/bin/sh

echo "Downloading client and server scripts"

rm remote-file-receiver.py
rm remote-file-sender.py

wget https://raw.githubusercontent.com/omegaui/remote-file-transfer/main/remote-file-receiver.py
wget https://raw.githubusercontent.com/omegaui/remote-file-transfer/main/remote-file-sender.py

echo "Done!"


