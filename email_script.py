import random
import itertools
import json
import time
import datetime


def readEmails(): 

    email_list = []

    with open('./contacts.csv', 'r') as file:
        for line in file:
            email = line.strip()
            rawData = email.split(',')

            if (rawData[0] != "ID"):
                email_list.append({"ID": rawData[0], "email": rawData[1], "name": rawData[2]})

    return email_list


def generateRandomPartners(emails):

    if len(emails) % 2 != 0:
        raise ValueError("The number of emails must be even to generate unique pairs.")
    
    pairs = []
    existingCombinations = getJson('partner_history.json')
    reorder = True

    while reorder:
        reorder = False
        random.shuffle(emails)
        pairs.clear

        for i in range(0, len(emails), 2):
                personA = emails[i]
                personB = emails[i + 1]
                pair = (personA, personB)

                if(checkExistingMatch(existingCombinations,pair)):
                        reorder = True
                
                pairs.append(pair)

    return pairs

def updatePartnerHistory(emails): 
    partnerHistory = getJson('partner_history.json')
    
    timestamp = time.time()
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    formatted_date = datetime_obj.strftime("%d.%m.%Y %H:%M:%S")

    for element in emails:
        numbers = sorted([
            int(element[0]["ID"]),
            int(element[1]["ID"])
        ])
        partnerHistory["matchesLogged"].append({
            "changeMakerA": numbers[0],
            "changeMakerB": numbers[1],
            "timestamp": formatted_date
        })


    updateJson(partnerHistory,'partner_history.json')

def updateJson(array,json_file): 
    with open(json_file, "w") as file:
        json.dump(array, file,indent=4)

def checkExistingMatch(data, combination):
    data = data["matchesLogged"]
    combination = sorted({
        int(combination[0]["ID"]),
        int(combination[1]["ID"]),
    })

    for elements in data:
        if elements["changeMakerA"] == combination[0] and elements["changeMakerB"] == combination[1]:
            return True

    return False


def getJson(json_file):
    try:
        with open(json_file, 'r') as file:
            return json.load(file)
    except json.JSONDecodeError as e:
            return []
        
emails = readEmails()
emails = generateRandomPartners(emails)


