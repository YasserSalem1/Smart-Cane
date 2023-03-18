#!/usr/bin/env python

import serial
import pyttsx3
import RPi.GPIO as GPIO
import random
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(38, GPIO.OUT)
GPIO.setup(40, GPIO.OUT)
engine = pyttsx3.init()
ser = serial.Serial("/dev/ttyAMA0", 115200)
distance_threshold = 1.5
strength_threshold = 1000
rand_direction = 1
min_speed = 50
max_speed = 100

def read_data():
    
    while True:
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.LOW)

        counter = ser.inWaiting()
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: 
                distance = bytes_serial[2] + bytes_serial[3] * 256 
                strength = bytes_serial[4] + bytes_serial[5] * 256
                # temperature = bytes_serial[6] + bytes_serial[7] * 256
                # temperature = (temperature/8) - 256
                distance = distance/50

                print("Signal strength is " + str(strength))
                print("Distance is " + str(distance) + " steps")

                if strength >= strength_threshold and distance <= distance_threshold:
                    distance = distance/50

                    if distance<1:
                        distance=1

                    text = "There is an obstacle  " + str(distance) + " steps to your front"
                    print(text)
                    print("Signal strength is " + str(strength))

                    GPIO.output(38, GPIO.LOW)
                    GPIO.output(40, GPIO.HIGH)

                    engine.say(text)
                    engine.runAndWait()

                    GPIO.output(38, GPIO.LOW)
                    GPIO.output(40, GPIO.LOW)

                    ser.reset_input_buffer()


if __name__ == "__main__":
    
    try:
        
        if ser.isOpen() == False:
            ser.open()

        read_data()

    finally:
        ser.close()
        GPIO.cleanup()