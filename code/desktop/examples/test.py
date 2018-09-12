from timing import *
from color import *

import pysher
import pusher
# Add a logging handler so we can see the raw communication data
import logging
import sys

import urllib.request, json

root = logging.getLogger()
root.setLevel(logging.INFO)
ch = logging.StreamHandler(sys.stdout)
root.addHandler(ch)

pusher_receiver = pysher.Pusher('334a34862786c44de127',cluster='eu', secret='b7220b4992a3f1b0ca0f')

pusher_sender = pusher.Pusher(app_id='586349', key='334a34862786c44de127', secret='b7220b4992a3f1b0ca0f', cluster='eu')

aPhrases = [
    "ready",
    "for",
    "data"
]
iPhrase = 0

def run(display):
    async def render():
        return await scheduleMessage(display)
    forever(render)

async def scheduleMessage(display):
    global iPhrase
    while iPhrase < len(aPhrases):

        red=0
        green=0
        blue=0

        sPhrase=str(aPhrases[iPhrase]["phrase"]).upper()
        print("working with phrase:" + str(iPhrase) + " of " + str(len(aPhrases)-1) + " -> "+ sPhrase )
        iPhrase+=1

        if(len(sPhrase)>9):
            print("phrase too long")
            continue

        display.clear(show=False)
        
        frameDelay = 0.1
        maxBrightness = 130

        for red in range(0, maxBrightness, 10):
            for _iIndex, cLetter in enumerate(sPhrase):
                character = display.characters[_iIndex]
                blue=red
                character.drawLetter(cLetter, [red, green, blue], show=False)

            display.show()
            await sleep(frameDelay)

        for green in range(0, maxBrightness, 10):
            for _iIndex, cLetter in enumerate(sPhrase):
                character = display.characters[_iIndex]
                red=255-green
                character.drawLetter(cLetter, [red, green, blue], show=False)

            display.show()
            await sleep(frameDelay)

        for _green in range(0, maxBrightness, 10):
            for _iIndex, cLetter in enumerate(sPhrase):
                character = display.characters[_iIndex]
                green=255-_green
                blue=green
                character.drawLetter(cLetter, [red, green, blue], show=False)

            display.show()
            await sleep(frameDelay)

    iPhrase=0


def fDownloadList():
    global aPhrases
    global iPhrase

    with urllib.request.urlopen("http://breadart.co.uk/clients/enlighten/server.list_phrases.php?idinstallations=1") as url:
        aPhrases = json.loads(url.read().decode())

    iPhrase=0

def  fListUpdate(*args, **kwargs):
    print("*** NEW LIST DOWNLOADED ***")
    fDownloadList()

def fRegister(oData):
    pusher_sender.trigger("enlighten", "hello", {'type':'artwork'})

# We can't subscribe until we've connected, so we use a callback handler
# to subscribe when able
def connect_handler(data):
    channel = pusher_receiver.subscribe('enlighten')
    channel.bind('new-phrase', fListUpdate)
    channel.bind('deleted-phrase', fListUpdate)
    channel.bind('deleted-phrase', fListUpdate)
    channel.bind('client-register', fRegister)

pusher_receiver.connection.bind('pusher:connection_established', connect_handler)
pusher_receiver.connect()

fDownloadList()
fRegister({})
