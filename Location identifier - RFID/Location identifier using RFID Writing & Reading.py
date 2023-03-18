#!/usr/bin/env python 

import RPi.GPIO as GPIO  
from mfrc522 import SimpleMFRC522  

reader = SimpleMFRC522()

while True:
    r_w = input("Read(r) or Write(w): ")
    r_w.lower()
    if r_w == "r":
        break
    elif r_w == "w":
        break
    else:
        print("Error ")

if r_w == "w":
    x = input("How many tags do you wish to write: ")
    x = int(x)
    for i in range(0, x):
        GPIO.cleanup()
        try:
            print("Name: ")
            name = input()
            print("Now place your tag to write")
            reader.write(name)
        except:
            print("Error while writing")
        else:
            print("Written")
        finally:
            GPIO.cleanup()

if r_w == "r":
    x = input("How many tags do you wish to read: ")
    x = int(x)
    for i in range(0, x):
        GPIO.cleanup()
        try:
            id, name = reader.read()
        except:
            print("Error while reading")
        else:
            print("ID is " + id)
            print("Name is " + name)
        finally:
            GPIO.cleanup()
