import pandas as pd
import ast
import random
import serial


def calculaterisk(temp, soilmoisture):
    print("Temperature is:",temp)
    print("Soil moisture reading of:",soilmoisture)
   
    heatwaverisk = 0

    # calc risk score from temp
    if temp < 10:
        heatwaverisk = heatwaverisk + 0
    elif temp >= 10 and temp < 20:
        heatwaverisk = heatwaverisk + 1
    elif temp >= 20:
        heatwaverisk = heatwaverisk + 2

    # combine risk score from moisture
    if soilmoisture >= 800:
        heatwaverisk = heatwaverisk + 0
    elif soilmoisture >= 650 and soilmoisture < 800:
        heatwaverisk = heatwaverisk + 1
    elif soilmoisture < 650: 
        heatwaverisk = heatwaverisk + 2

    # convert risk score to text
    if heatwaverisk == 0:
        print("No risk of heatwave")
    elif heatwaverisk == 1:
        print("Very low risk of heatwave")
    elif heatwaverisk == 2:
        print("low risk of heatwave")
    elif heatwaverisk == 3:
        print("Risk of heatwave")
    else:
        print("Significant risk of heatwave")


def riskanalysis():

    #Advanced requirement 1 - disaster risk modelling
    print("Microbit readings")
    dt = pd.read_csv("microbitmoisture.csv",)
    soilmoisture = dt["Moisture"].iloc[99]
    temp = dt["Temperature"].iloc[99]
    calculaterisk(temp, soilmoisture)
    print("-----------")

    #Advanced requirement 2 - what-if scenarios
    print("What-if temperature increases by 10 degrees")
    temp = temp + 10
    calculaterisk(temp, soilmoisture)
    print("-----------")
    
    print("What-if soil moisture decreases by 50%")
    soilmoisture = soilmoisture / 2
    calculaterisk(temp, soilmoisture)
    print("-----------")
    
    print("Adaptive - read live temp/soil moisture")
    ser = serial.Serial("COM3", 115200)
    for i in range(10):
        data = ser.readline().decode("utf-8").strip()
        separate_data = data.split(",")
        if len(separate_data) == 2:
            temp = separate_data[0]
            soilmoisture = separate_data[1]
            calculaterisk(temp, soilmoisture)

riskanalysis()
