#whatsapp chat analyser
#features:
#1. number of messages per user
#2. first text sent on 
#3. Each User's first message
#4. Most used word
import pandas as pd
import numpy as np
import regex as re
import csv
from contextlib import redirect_stdout
import collections
def startsWithDateAndTime(s):
    # regex pattern for date.(Works only for android. IOS Whatsapp export format is different. Will update the code soon
    pattern = '^([0-9]+)(\\/)([0-9]+)(\\/)([0-9][0-9]), ([0-9]+):([0-9][0-9]) (AM|PM) -'
    result = re.match(pattern, s)
    if result:
        return True
    return False  
# Finds username of any given format.
def FindAuthor(s):
    patterns = [
        '([\\w]+):',                        # First Name
        '([\\w]+[\\s]+[\\w]+):',              # First Name + Last Name
        '([\\w]+[\\s]+[\\w]+[\\s]+[\\w]+):',    # First Name + Middle Name + Last Name
        '([+]\\d{2} \\d{5} \\d{5}):',         # Mobile Number (India)
        '([+]\\d{2} \\d{3} \\d{3} \\d{4}):',   # Mobile Number (US)
        '([\\w]+)[\u263a-\U0001f999]+:',    # Name and Emoji              
    ]
    pattern = '^' + '|'.join(patterns)
    result = re.match(pattern, s)
    if result:
        return True
    return False  
def getDataPoint(line):   
    splitLine = line.split(' - ') 
    dateTime = splitLine[0]
    date, time = dateTime.split(', ') 
    message = ' '.join(splitLine[1:])
    if FindAuthor(message): 
        splitMessage = message.split(': ') 
        author = splitMessage[0] 
        message = ' '.join(splitMessage[1:])
    else:
        author = None
    return date, time, author, message
parsedData = [] # List to keep track of data so it can be used by a Pandas dataframe
# Upload your file here
conversationPath = '' # enter path of .txt chat file
with open(conversationPath, encoding="utf-8") as fp:
    fp.readline() # Skipping first line of the file because contains information related to something about end-to-end encryption
    messageBuffer = [] 
    date, time, author = None, None, None
    while True:
        line = fp.readline() 
        if not line: 
            break
        line = line.strip() 
        if startsWithDateAndTime(line): 
            if len(messageBuffer) > 0: 
                parsedData.append([date, time, author, ' '.join(messageBuffer)]) 
            messageBuffer.clear() 
            date, time, author, message = getDataPoint(line) 
            messageBuffer.append(message) 
        else:
            messageBuffer.append(line)   
df = pd.DataFrame(parsedData, columns=['Date', 'Time', 'Author', 'Message']) # Initialising a pandas Dataframe.
df["Date"] = pd.to_datetime(df["Date"])
df.to_csv('.csv') #enter path with name to save you .csv file

#1. counting the number of messages from each user
data = pd.read_csv("") #same path as in line n0. 69
AP=0
XX=0
for x in data["Author"]:
    if x=="": YY+=1 #your name
    elif x=="" : XX+=1 #other person's name
#2. first text sent on
#3. Most used words
MUW = pd.Series(' '.join(df['Message']).lower().split()).value_counts()[:10]
with open('C:\\Users\\Ankan-HP\\Desktop\\Python\\Python Projects\\whatsapp_analyser_output', 'w',encoding="utf-8") as f:
    with redirect_stdout(f):
        print("Number of messages sent by :",YY,"\n")
        print("Number of messages sent by :",XX,"\n")
        print("First message sent on:",data['Date'].iloc[1],"at",data['Time'].iloc[2],"\n")
        print("First message was sent by:",data['Author'].iloc[1],"\n")
        print("First message was:",data['Message'].iloc[1],"\n")
        print("Top 10 most used words are:\n",MUW)

