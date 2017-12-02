Example routine to install and launch

# Mac

Install homebrew, then...

brew install python3
pip3 install graphics.py
pip3 install numpy

cd desktop
export PYTHONPATH=.
python3 examples/helloworld.py

# Linux (Ubuntu 16.10 Yakkety)

sudo apt install python3.6 python3-tk mosquitto mosquitto-clients
sudo service mosquitto restart
sudo python3.6 -m pip install --upgrade --force-reinstall graphics.py numpy hbmqtt
cd code/desktop 
python3.6 examples/publishdisplay.py

# Raspbian

Install BerryConda3 to give Python3, then follow Linux guidance


