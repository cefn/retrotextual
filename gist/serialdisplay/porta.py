import serial
import experiment
portA = serial.Serial(baudrate=experiment.baudrate, port='/dev/ttyUSB0')
count = 0
while True:
	portA.write(str(count).encode("ascii"))
	portA.write(b'\n')
	count += 1
