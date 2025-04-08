#!/usr/bin/python

import sys
import time
import schedule
import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime

def do_the_watering(isItGonnaRain, isThereWaterInTheBarrel):
    print("Checking if it's time to water")
    if (isThereWaterInTheBarrel is True and isItGonnaRain is False):
        unleash_the_water()

def unleash_the_water():
    print("Doing the watering")
    lastWateredTime = datetime.now()
    push_data("lastWateredTime", lastWateredTime)

def check_weather():
    #Only looking for rain in the next hour
    print("Checking weather")
    return False

def check_barrel_water():
    #As long as the water in the barrel is at a certain amount, return True
    print("Checking barrel water")
    barrelWater = inquire_the_barrel()
    if (barrelWater > 10):
        return True
    else:
        return False

def inquire_the_barrel():
    barrel_water = 100
    return barrel_water

def inquire_the_ground():
    ground_water = 100
    return ground_water

def manual_watering():
    #If manual watering is true, initiate watering and then update flag to false
    print("Checking for manual watering option")
    manualWatering = pull_data("manualWatering")
    isThereWaterInTheBarrel = check_barrel_water()
    if (manualWatering == True and isThereWaterInTheBarrel == True):
        print("Manual Watering is true")
        unleash_the_water()
    else:
        print("Manual Watering is false")

def main_loop():
    print("Running main loop")
    isItGonnaRain = check_weather()
    isThereWaterInTheBarrel = check_barrel_water()
    do_the_watering(isItGonnaRain, isThereWaterInTheBarrel)

def pull_data(searchTerm):
    print("Pulling data")
    try:
        doc_ref = db.collection('configuration').document('aOPXgxYsXLhtzX5ft7Dl')
        doc = doc_ref.get()
        if doc.exists:
            user_data = doc.to_dict()  # Get the document data as a dictionary
            value = user_data.get(searchTerm)  # Access the "name" field
            return value
        else:
            print(u'No such document!')
    except Exception as e:
        print(f"Error getting document: {e}")
        return None
    
def push_data(searchTerm, data):
    print("Sending data")
    try:
        doc_ref = db.collection('configuration').document('aOPXgxYsXLhtzX5ft7Dl')
        doc_ref.update({searchTerm: data})
    except Exception as e:
        print(f"Error getting document: {e}")
        return None

def regular_water_check():
    #Checking water in barrel. Will alert if low
    print("Checking water amount in barrel")
    waterLevel = inquire_the_barrel()
    push_data("waterLevel", waterLevel)

def regular_moisture_check():
    #Checking the moisture of the soil. Will alert if low. This may be cause 
    #for a manual watering
    print("Checking the moisture of the soil")
    moistureLevel = inquire_the_ground()
    push_data("moistureLevel", moistureLevel)

def restartCheck():
    autoRestart = pull_data("autoRestart")
    if (autoRestart == True):
        print("Auto Restart is true")
    else:
        print("Auto Restart is false")

schedule.every().hour.do(regular_water_check)
schedule.every().hour.do(regular_moisture_check)
schedule.every().hour.do(manual_watering)
schedule.every().hour.do(restartCheck)
schedule.every().day.at("08:00").do(main_loop)
schedule.every().day.at("13:00").do(main_loop)
schedule.every().day.at("17:00").do(main_loop)

if __name__ == '__main__':
    try:
        print("Welcome to HepGrow")
        cred = credentials.Certificate('authentication/auth.json')
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        while True:
            schedule.run_pending()
            time.sleep(30)
    except KeyboardInterrupt:
        print('Exiting by user request')
        sys.exit(0)