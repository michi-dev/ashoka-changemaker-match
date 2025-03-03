import random
import itertools
import json
import time
import datetime
import sys
import mailer
import imageEncoder

def readEmails(): 

    email_list = []

    with open('./contacts/contacts.csv', 'r') as file:
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
    existingCombinations = getJson('contacts/partner_history.json')
    reorder = True
    startTime = time.time()
    print("Starting Search..")
    while reorder:
        if (time.time() - startTime) > 30:
            print("Die Suche hat über dreissig Sekunden gedauert. Bitte prüfe, ob nicht bereits alle Changemaker gemached wurden.")
            sys.exit()
            
        reorder = False
        random.shuffle(emails)
        pairs = []

        for i in range(0, len(emails), 2):
                personA = emails[i]
                personB = emails[i + 1]
                pair = (personA, personB)

                if(checkExistingMatch(existingCombinations,pair)):
                        reorder = True
                else:
                    updatePartnerHistory(pair)
                pairs.append(pair)


    return pairs

def updatePartnerHistory(element): 
    partnerHistory = getJson('contacts/partner_history.json')
    
    timestamp = time.time()
    datetime_obj = datetime.datetime.fromtimestamp(timestamp)
    formatted_date = datetime_obj.strftime("%d.%m.%Y %H:%M:%S")

    numbers = sorted([
        int(element[0]["ID"]),
        int(element[1]["ID"])
    ])

    partnerHistory["matchesLogged"].append({
        "changeMakerA": numbers[0],
        "changeMakerB": numbers[1],
        "timestamp": formatted_date
    })


    updateJson(partnerHistory,'contacts/partner_history.json')

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

def notifyPeople(matches):
    for match in matches:
        for i in range(len(match)):
            email_content = renderHTMLTempalte(
                {
                    "{{MatchName}}": '✨' + match[i]["name"] + '✨',
                    "{{MatchEmail}}": match[i]["email"],
                    "{{MatchImage}}": imageEncoder.encodeImage("images/" + match[i]["ID"] + ".jpeg")
                },
                'templates/email_template.html'
            )
            
            if i is 0:
                x = 1
            else:
                x = 0

            mailer.sendmail(match[x]["email"],'Dein Changemaker-Match mit ' + match[i]["name"] + '🥳', email_content)

def generateMatchingReport(matches):
    for match in matches:
        print(match[0]["name"] + " matched with " + match[1]["name"])

def renderHTMLTempalte(vars,template_file): 
    works = False

    with open(template_file, 'r') as file:
        template = file.read()
        works = True

    if(works):
        for key, value in vars.items():
            template = template.replace(key, value.strip())
        
    return template




emails = readEmails()
emails = generateRandomPartners(emails)
notifyPeople(emails)
#generateMatchingReport(emails)

