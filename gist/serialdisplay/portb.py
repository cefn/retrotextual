import serial
import experiment
portB = serial.Serial(baudrate=experiment.baudrate,port='/dev/ttyUSB1')
while True:
	line = portB.readline()
	print(line)
