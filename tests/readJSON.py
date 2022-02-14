import json
import time
from datetime import datetime

deviceList = ['bloodPressure.json', 'weight.json', 'glucometer.json', 'pulse.json', 'oximeter.json', 'thermometerSchema.json']
knownValues = {'device': ['blood pressure', 'weight', 'glucometer', 'pulse', 'oximeter', 'thermometer'], 'patient_ID': ['1224', '1233', '2234', '3231'],
'issuer': ['Johnson & Johnson', 'Abbott', 'Medtronic', 'Baxter', 'GE'], 'serial_number': ['HES122344', 'KDE223234', 'JJS124523', 'FHE903929'], 'issue_date': '04-30-21', 'status': ['active', 'inactive']}

import time
def is_date_valid(year, month, day):
    this_date = '%d/%d/%d' % (month, day, year)
    try:
        time.strptime(this_date, '%m/%d/%Y')
    except ValueError:
        return False
    else:
        return True

def test1():
    for device in deviceList:
        # Opening JSON file
        f = open(device)
        
        # returns JSON object as
        # a dictionary
        data = json.load(f)
        
        # Iterating through the json
        # list
        for key, value in data.items():
            if key == 'reading':
                assert value.isdigit(), "Reading must be a digit"
            elif key == 'issue_date':
                format = "%d-%m-%Y"
                res = True
 
                # using try-except to check for truth value
                try:
                    res = bool(datetime.strptime(value, format))
                except ValueError:
                    res = False
                assert res, "Invalid Date Format"
            elif value not in knownValues[key]:
                assert False, "Value not in database"
        
        # Closing file
        f.close()

if __name__ == '__main__':
    test1()