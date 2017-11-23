This emulator provides a graphical equivalent to the WS2811 LED arrays, driven as a 'display' client by the same protocol (mediated by an MQTT broker), and hence suitable for verifying the behaviour of user-designed regimes running in a suitable 'driver' client.

Driver clients are expected to be launched and killed on an ad-hoc basis, although only one should be running at a time. This means they can be run as single-threaded Asyncio python scripts, without any overall management. 

Scheduling becomes a matter of killing a script already running, and launching a new script.

To run this emulator, make sure the following install steps have been run...

pip3 install hbmqtt
pip3 install graphics.py
...which requires tk...
[on Ubuntu] sudo apt install python3-tk

