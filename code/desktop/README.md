Example routine to install and launch

# Linux (Ubuntu 16.10 Yakkety)

sudo apt install python3.6 python3-tk mosquitto mosquitto-clients
sudo python3.6 -m pip install --upgrade --force-reinstall graphics.py numpy hbmqtt
cd code/desktop 
python3.6 examples/publishdisplay.py

# Mac
[On a Mac] Install homebrew

brew install python3
pip3 install graphics.py
pip3 install numpy

cd desktop
export PYTHONPATH=.
python3 examples/helloworld.py
