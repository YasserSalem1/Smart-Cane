#!/usr/bin/env python

import pandas as pd
import pyttsx3
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522

engine = pyttsx3.init()
reader = SimpleMFRC522()
NULL = -1
pre = NULL
GPIO.cleanup()

try:
    nfc_id, name = reader.read()

except:

    engine.say("Error while reading")
    engine.runAndWait()

else:
        our_id = name[len(name) - 2] + name[len(name) - 1]

        if our_id.isnumeric() == True:
            our_id = int(our_id)

            if  1 <= our_id <= 25:
                dataframe = pd.read_excel("/home/jamal/Cane/RFID/Building_NFC_Dataset_Code_Format.xlsx")
                dfcolumn = dataframe.iloc[our_id - 1]
                column = dfcolumn.values.tolist()  # type: ignore
                column_free=[i for i in column if i!="&"]

                if pre == NULL:
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()

                    if column[2] != "&":
                        text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                        engine.say(text)
                        engine.runAndWait()

                    if column[4] != "&":
                        text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                        engine.say(text)
                        engine.runAndWait()

                    if column[6] != "&":
                        text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                        engine.say(text) 
                        engine.runAndWait()

                    if column[8] != "&":
                        text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                        engine.say(text)
                        engine.runAndWait() 

                elif pre == 18 and our_id == 19:
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()
                    front = column[2]
                    front_steps = column[3]

                    if front_steps == "&":

                        if column[2] != "&":
                            text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[4] != "&":
                            text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[6] != "&":
                            text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[8] != "&":
                            text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                    else:
                        text = str(front_steps) + " Steps to Your Front is " + str(front)
                        engine.say(text)
                        engine.runAndWait()

                elif pre == 19 and our_id == 18:
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()
                    front = column[4]
                    front_steps = column[5]

                    if front_steps == "&":

                        if column[2] != "&":
                            text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[4] != "&":
                            text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[6] != "&":
                            text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[8] != "&":
                            text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                    else:
                        text = str(front_steps) + " Steps to Your Front is " + str(front)
                        engine.say(text)
                        engine.runAndWait()

                elif pre == our_id:
                    column[2], column[3], column[4], column[5] = column[4], column[5], column[2], column[3]
                    column[6], column[7], column[8], column[9] = column[8], column[9], column[6], column[7]
                    column_free=[i for i in column if i!="&"]
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()

                    if column[2] != "&":
                        text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                        engine.say(text)
                        engine.runAndWait()

                    if column[4] != "&":
                        text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                        engine.say(text)
                        engine.runAndWait()

                    if column[6] != "&":
                        text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                        engine.say(text)
                        engine.runAndWait()

                    if column[8] != "&":
                        text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                        engine.say(text)
                        engine.runAndWait()

                elif (pre-2) >=  our_id:   
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()
                    front = column[4]
                    front_steps = column[5]

                    if front_steps == "&":

                        if column[2] != "&":
                            text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[4] != "&":
                            text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()

                        if column[6] != "&":
                            text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                            engine.say(text)
                            engine.runAndWait() 
                        
                        if column[8] != "&":
                            text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                    
                    else:
                        text = str(front_steps) + " Steps to Your Front is " + str(front)
                        engine.say(text)
                        engine.runAndWait()
                
                elif (pre+2) <=  our_id:
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()
                    front = column[2]
                    front_steps = column[3]
                    
                    if front_steps == "&":
                        
                        if column[2] != "&":
                            text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                        
                        if column[4] != "&":
                            text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                        
                        if column[6] != "&":
                            text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                            engine.say(text) 
                            engine.runAndWait()
                        
                        if column[8] != "&":
                            text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                    
                    else:
                        text = str(front_steps) + " Steps to Your Front is " + str(front)
                        engine.say(text)
                        engine.runAndWait()
                
                elif (pre+1) ==  our_id: 
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()
                    front = column[8]
                    front_steps = column[9]
                    
                    if front_steps == "&":
                        
                        if column[2] != "&":
                            text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                        
                        if column[4] != "&":
                            text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                        
                        if column[6] != "&":
                            text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                            engine.say(text) 
                            engine.runAndWait()
                        
                        if column[8] != "&":
                            text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                    
                    else:
                        text = str(front_steps) + " Steps to Your Front is " + str(front)
                        engine.say(text)
                        engine.runAndWait()
                
                elif (pre-1) ==  our_id:   
                    at = column[1]
                    at = at[:-3]
                    text = "You are at " + at
                    engine.say(text)
                    engine.runAndWait()
                    front = column[6]
                    front_steps = column[7]
                    
                    if front_steps == "&":
                        
                        if column[2] != "&":
                            text = "To Your East is " + column[2] + "By " + str(column[3]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                        
                        if column[4] != "&":
                            text = "To Your West is " + column[4] + "By " + str(column[5]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                        
                        if column[6] != "&":
                            text = "To Your North is " + column[6] + "By " + str(column[7]) + " Steps"
                            engine.say(text) 
                            engine.runAndWait()
                        
                        if column[8] != "&":
                            text = "To Your South is " + column[8] + "By " + str(column[9]) + " Steps"
                            engine.say(text)
                            engine.runAndWait()
                    
                    else:
                        text = str(front_steps) + " Steps to Your Front_is_" + str(front)
                        engine.say(text)
                        engine.runAndWait()

                pre = our_id

finally:
        GPIO.cleanup()
