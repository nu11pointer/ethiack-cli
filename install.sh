#!/bin/bash

pip3 install -r requirements.txt
chmod +x "$(pwd)/ethiack.py"
sudo ln -s "$(pwd)/ethiack.py" /usr/local/bin/ethiack
echo
echo "DONE!"
echo
echo "Usage: ethiack help"