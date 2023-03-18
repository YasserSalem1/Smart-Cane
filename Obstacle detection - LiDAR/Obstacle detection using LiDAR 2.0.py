#!/usr/bin/env python

import serial
import pyttsx3
import RPi.GPIO as GPIO
import random

GPIO.setmode(GPIO.BCM)
pinLeft = 31
pinRight = 32
GPIO.setup(pinLeft, GPIO.OUT)
GPIO.setup(pinRight, GPIO.OUT)
engine = pyttsx3.init()
ser = serial.Serial("/dev/ttyAMA0", 115200)
left = GPIO.PWM(pinLeft, 50)
right = GPIO.PWM(pinRight, 50)
distance_threshold = 70
strength_threshold = 100
rand_direction = random.randint(0, 1)
min_speed = 0
max_speed = 30

def read_data():
    while True:
        counter = ser.in_waiting
        if counter > 8:
            bytes_serial = ser.read(9)
            ser.reset_input_buffer()

            if bytes_serial[0] == 0x59 and bytes_serial[1] == 0x59: 
                distance = bytes_serial[2] + bytes_serial[3] * 256 
                strength = bytes_serial[4] + bytes_serial[5] * 256
                # temperature = bytes_serial[6] + bytes_serial[7] * 256
                # temperature = (temperature/8) - 256
                print("Signal strength is " + str(strength))
                print("Distance is " + str(distance) + " cm")
                if strength >= strength_threshold and distance <= distance_threshold:
                    text = "There is an obstacle  " + str(distance) + " centimeters to your front"
                    print(text)
                    print("Signal strength is " + str(strength))
                    engine.say(text)
                    if rand_direction == 1:
                        left.start(min_speed)
                        for i in range(min_speed,max_speed):
                            left.ChangeDutyCycle(i)
                            if strength >= strength_threshold and distance > distance_threshold:
                                left.stop()
                                break
                        left.stop()
                    elif rand_direction == 0:
                        right.start(min_speed)
                        for i in range(min_speed,max_speed):
                            right.ChangeDutyCycle(i)
                            if strength >= strength_threshold and distance > distance_threshold:
                                right.stop() 
                                break
                        right.stop() 
                    GPIO.cleanup()
                ser.reset_input_buffer()

if __name__ == "__main__":
    try:
        if ser.isOpen() == False:
            ser.open()
        GPIO.cleanup()
        read_data()
    except KeyboardInterrupt: # ctrl + c in terminal.
        if ser != None:
            ser.close()
        GPIO.cleanup()
        print("Program interrupted by the user")
    finally:
        GPIO.cleanup()