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
import gc

class UartLights:
    def __init__(self, pixelCount, baud=57600, numColorBytes = 3):
        self.pixelCount = pixelCount
        self.uart = UART(1, baud)
        self.frameLength = pixelCount * numColorBytes
        assert self.frameLength < 128 # a single byte is used to set the frame size

    def sendColorBytes(self, buffer):
        self.uart.write(bytes([self.frameLength]))
        self.uart.write(buffer)
        gc.collect()


pixelCount = 16
lights = UartLights(pixelCount=pixelCount, baud=57600, numColorBytes=3)

def primaryRegime():
    from utime import sleep_ms, ticks_ms, ticks_diff

    frameCount = 0

    regimeStartMs = ticks_ms()

    red = (255,0,0)
    green = (0,255,0)
    blue = (0,0,255)
    yellow = (255,255,0)
    colors = (red, green, blue, yellow)
#    fixed = green
#    colors = (fixed, fixed, fixed, fixed)

    def frameGeneratorFactory(pixelCount):
        for pixelPos in range(pixelCount):
            yield from colors[(pixelPos + frameCount) % 4]
        yield ord('\n')

    while True:
        startFrameMs = ticks_ms()
        lights.sendColorBytes(bytes(frameGeneratorFactory(pixelCount)))
        endFrameMs = ticks_ms()
        frameCount += 1
        print("{}, {}, {}".format(frameCount, ticks_diff(endFrameMs, startFrameMs), (frameCount * 1000)/ ticks_diff(endFrameMs, regimeStartMs)))
        sleep_ms(500)

if __name__ == "__main__":
    primaryRegime()