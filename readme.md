# Functionality
## Input
1. Reads contacts from contacts/contacts.csv
2. Gets and encodes pictures from images/ (if there is no image - takes default one)
3. Gets the email template with styling from templates/email_template.html
4. Gets the matching history with previous matching from  contacts/partner_history.json


## Processing
1. Loops through all contacts and generates random matches
2. checks if the matches exist in contacts/partner_history.json
3. if yes: repeats step 1 & 2

if the script cant find unique matches for 30 secs it stopps and informs the user that the history has to be cleared, because all matches were previously made


## Output
1.  sends emails to unique matches to inform them about their partner (using name, email and image)


# requirements
## Check if python is installed

```
python3 --version
```

## Install pillow

```
pip install pillow
```

# important
- images have to be .jpeg to be encoded correctly!
- make sure to have no empty lines in the .csv file
- the ID of the person in the .csv has to be the filename of the persons image

# Example

```contacts/contacts.csv```
```
ID,email,Name
1,test.test@email.net,Max Muster
```

```images/1.jpeg``` --> Picture of Max Muster
