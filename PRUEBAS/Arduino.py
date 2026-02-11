import serial
import time

# Cambia 'COM3' por el puerto de tu Arduino
puerto = '/dev/ttyUSB0'
velocidad = 9600
arduino = serial.Serial(puerto, velocidad, timeout=1)
time.sleep(2)  # Esperar a que el Arduino reinicie

while True:
    if arduino.in_waiting > 0:
        linea = arduino.readline().decode('utf-8').strip()
        print(linea)