#PYTHON 3

#import necessary libraries
import urllib
import datetime

#import BeautifulSoup functions
from bs4 import BeautifulSoup

#Print today's date and time and store current time hours and minutes
fullDate = datetime.datetime.now()

print("Current Date: " + fullDate.strftime("%A %d %B"))
print("Current Time: " + fullDate.strftime("%H:%M"))
print("\n")

nowHour = int(fullDate.hour)
nowMinute = int(fullDate.minute)

#Find and parse page data from specified URL
url = "http://m.metservice.com/marine/tides/auckland"
page = urllib.request.urlopen(url)
pageData = BeautifulSoup(page, features="lxml")

#Find data: the tables and the titles of each 
#TO DO: INSERT A CHECK FOR THIS NOT WORKING ("no tide data is available")
allTables = pageData.find_all('table')
allTitles = pageData.find_all('h3')

#Gather first 3 tables and titles
titles = [title.find(text = True) for title in allTitles[0:4]]
tables = allTables[0:4]

def findMinutesDifference(hour1, minute1, hour2, minute2):
    return abs(hour1 * 60 - hour2 * 60 + minute1 - minute2)

#FOLLOWING IS ONLY APPLICABLE TO FIRST TABLE

#Cycle through the rows, and extract the necessary info from the first two columns
dataRows = tables[0].find_all('tr')[1:] #Each index stores all the info within a row tag

labels = []
times = []

for row in dataRows:
    dataCols = row.find_all('td') #For each row tag info found, store all the info within each column tag
    
    labels.append(str(dataCols[0].find(text = True)))
    times.append(str(dataCols[1].find(text = True)))    

#Find the index positions of HIGH in the labels list
highPositions = [i for i,x in enumerate(labels) if x == 'HIGH']

#Create two lists, one storing the hour value and one storing the minute value of each tide time
tideHour = [int(time[0] + time[1]) for time in times]
tideMinute = [int(time[3] + time[4]) for time in times]

#Calculation of current distance from a high tide
minutesDifference1 = findMinutesDifference(nowHour, nowMinute, tideHour[highPositions[0]], tideMinute[highPositions[0]])
if len(highPositions) == 1: #There was only 1 high tide today, already calculated
    
    print("**We are " + str(minutesDifference1//60) + " hours and " + str(minutesDifference1%60) + " minutes away from a high tide**")

elif len(highPositions) == 2: #There were 2 high tides, need to find which was closest
    
    minutesDifference2 = findMinutesDifference(nowHour, nowMinute, tideHour[highPositions[1]], tideMinute[highPositions[1]])
    
    #Check which time difference is smaller, and output appropriate message
    if (minutesDifference1 <= minutesDifference2):
        print("**We are " + str(minutesDifference1//60) + " hours and " + str(minutesDifference1%60) + " minutes away from a high tide**")
    else:
        print("**We are " + str(minutesDifference2//60) + " hours and " + str(minutesDifference2%60) + " minutes away from a high tide**")
        
#Print Today's Output for user
print("\n")
if len(highPositions) == 0:
    print("There is no high tide today") #unrealistic output, but just in case
elif len(highPositions) == 1:
    print("High tide today is at " + times[highPositions[0]])
else:
    print("High tide today is at " + times[highPositions[0]] + " and " + times[highPositions[1]])

    
#Print the next 3 day's data
for index in range(1, 4):
    
    #Cycle through the rows, and extract the necessary info from the first two columns
    dataRows = tables[index].find_all('tr')[1:] #Each index stores all the info within a row tag

    labels = []
    times = []

    for row in dataRows:
        dataCols = row.find_all('td') #For each row tag info found, store all the info within each column tag
    
        labels.append(str(dataCols[0].find(text = True)))
        times.append(str(dataCols[1].find(text = True)))    

    #Find the index positions of HIGH in the labels list
    highPositions = [i for i,x in enumerate(labels) if x == 'HIGH']
    
    print("\n")
    print(titles[index])
    if len(highPositions) == 0:
        print("There is no higtide") #unrealistic output, but just in case
    elif len(highPositions) == 1:
        print("High tide is at " + times[highPositions[0]])
    else:
        print("High tide is at " + times[highPositions[0]] + " and " + times[highPositions[1]])