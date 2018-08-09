'''
Typical throughput results - number of frames, ms for serial send and frames per second
780, 7, 0.0659898
781, 10, 0.0659851
782, 9, 0.0659804
783, 12, 0.065959
784, 8, 0.0659599
785, 8, 0.0659664
786, 8, 0.0659673
787, 8, 0.0659737
788, 8, 0.0659745
789, 9, 0.0659754
790, 8, 0.0659818
791, 10, 0.0659716
792, 8, 0.0659725
793, 11, 0.0659569
794, 8, 0.0659578
795, 8, 0.0659587
796, 8, 0.065965
'''

from machine import UART
import network
import gc

class UartLights:
    def __init__(self, pixelCount=16, baud=115200, bytesPerPixel = 3):
        assert pixelCount < 256 # a single byte is used to set the pixelcount
        self.uart = UART(1, baud)
        self.header = bytes([pixelCount])   # set the leading byte to be permanently the pixelCount
        self.buffer = bytearray(pixelCount * bytesPerPixel) # a byte each for red, green, blue
        self.footer = bytes([ord('\n')])    # set the trailing byte to be permanently newline

    def sendColorBytes(self):
        self.uart.write(self.header)
        self.uart.write(self.buffer)
        self.uart.write(self.footer)

def primaryRegime():
    wlan = network.WLAN()
    wlan.disconnect()

    bytesPerPixel = 3
    pixelCount = 16
    baud = 115200

    lights = UartLights(pixelCount=pixelCount, baud=baud, bytesPerPixel=bytesPerPixel)
    from utime import sleep_ms, ticks_ms, ticks_diff

    frameCount = 0
    regimeStartMs = ticks_ms()

    red = b'\xff\x00\x00'
    green = b'\x00\xff\x00'
    blue = b'\x00\x00\xff'
    yellow = b'\x00\xff\xff'
    colors = (red, green, blue, yellow)

    while True:
        for pixelPos in range(0, pixelCount):
            bufferPos = pixelPos * bytesPerPixel
            offset = (pixelPos + frameCount) % 4 # len(colors)?
            lights.buffer[bufferPos:bufferPos+bytesPerPixel] = colors[offset]
        lights.sendColorBytes()
        endFrameMs = ticks_ms()
        frameCount += 1
        if frameCount % 100 == 0:
            print((frameCount * 1000)/ ticks_diff(endFrameMs, regimeStartMs))
        gc.collect()

if __name__ == "__main__":
    primaryRegime()
