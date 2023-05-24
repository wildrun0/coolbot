#!/bin/sh

SCRIPT=$(readlink -f "$0")
SCRIPTPATH=$(dirname "$SCRIPT")


if python3.10 --version 2>&1; then
	echo Python 3.10 detected
else
	echo Python 3.10 not found! Exiting...
	exit 1
fi

if [ ! -d "$SCRIPTPATH/.venv/" ]; then
	echo creating python virtual env
	python3.10 -m venv $SCRIPTPATH/.venv
fi

echo Installing dependencies...
$SCRIPTPATH/.venv/bin/python -m pip install -r $SCRIPTPATH/req.txt

echo Creating coolbot service daemon
echo "[Unit]
Description=Coolbot VK daemon service

[Service]
Type=idle
User=root
WorkingDirectory=$SCRIPTPATH
ExecStart=$SCRIPTPATH/.venv/bin/python coolbot.py

[Install]
WantedBy=multi-user.target" | sudo tee --append /etc/systemd/system/coolbot.service

echo Reloading systemctl daemon
sudo systemctl daemon-reload

while true; do
    read -p "Do you wish to enable coolbot at every system boot? " yn
    case $yn in
        [Yy]* ) sudo systemctl enable coolbot.service; break;;
        [Nn]* ) exit;;
        * ) echo "Please answer yes or no.";;
    esac
done

echo Starting a coolbot service
sudo systemctl start coolbot.service

echo Done! Coolbot is running
