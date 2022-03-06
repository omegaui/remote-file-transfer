#!/bin/sh

echo "Downloading client and server scripts"

curl https://raw.githubusercontent.com/omegaui/remote-file-transfer/main/.release -o remote-file-sender.py
curl https://raw.githubusercontent.com/omegaui/remote-file-transfer/main/.release -o remote-file-receiver.py

echo "Done!"


