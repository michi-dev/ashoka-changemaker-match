import random
import itertools
import json

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

                if personA["ID"] in existingCombinations:
                    if personB["ID"] in existingCombinations[personA["ID"]]:
                        reorder = True

                pairs.append(pair)

    return pairs

def updatePartnerHistory(emails): 
    partnerHistory = getJson('partner_history.json')
    
    for element in emails:
        print(element["ID"])

def updateJson(array,json_file): 
    with open(json_file, "w") as file:
        json.dump(array, file)


def getJson(json_file):
    with open(json_file, 'r') as file:
        return json.load(file)

emails = readEmails()
emails = generateRandomPartners(emails)
updatePartnerHistory(emails)


