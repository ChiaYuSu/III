# Import modules
import json
import ssl
import urllib.request as request
import re
import matplotlib.pyplot as plt
import numpy as np
import statistics
import pandas as pd
import matplotlib.ticker as ticker
from datetime import datetime

# Input case
num = "Real42"
case = "Case " + num

# For SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200928/" + num + "/output.json"

# TFC timestamp
timestamp = 1601308800  # Draw tfc check time line
endTime = int(str(1602475200))  # Adjust case end timestamp

# Read json
with request.urlopen(src) as response:
    data = json.load(response)

# Json sorted by time
data = sorted(data, key=lambda k: k['time'])

# Find out the start and end time of the case
lists = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < endTime:
        lists.append(str(i["time"]))
start = int(str(min(lists))) #
end = int(str(max(lists))) #

# # Write json to file (For debugging)
# with open('case.json', mode='w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)

# Unix Timestamp list for plot (1 month)
unixTimestampPlot = []
stampCount = int(((end - start) / 2592000) + 1)  # 86400 * 30 = 2892000
for i in range(stampCount):
    unixTimestampPlot.append(start + i * 2592000)

# Unix Timestamp list for x-axis label (6 month)
unixTimestampXaxis = []
for i in range(len(unixTimestampPlot)):
    if i % 6 == 0:
        unixTimestampXaxis.append(unixTimestampPlot[i])
   
# Format Unix Timestamp to DateTime (1 month)
dateTimeMonth = []
for i in unixTimestampPlot:
    dateTimeMonth.append(datetime.utcfromtimestamp(i).strftime('%Y-%m-%d'))

# Format Unix Timestamp to DateTime (6 month)
dateTimeHalfYear = []
for i in unixTimestampXaxis:
    dateTimeHalfYear.append(datetime.utcfromtimestamp(i).strftime('%Y-%m-%d'))

# Calculate the number of nodes for each approximation
amount = []
count = 0
for i in range(stampCount - 1):
    for j in data:
        if j["type"] == "article" and int(j["time"]) >= unixTimestampPlot[i] and int(j["time"]) <= unixTimestampPlot[i+1]:
            count += 1
    amount.append(count)
    count = 0
amount.append(0)

# Average number of nodes per month
amountAvg = sum(amount) / len(unixTimestampPlot)

# Find the largest value in amount list and its index
nodeMax = amount.index(max(amount))
largestTime = unixTimestampPlot[nodeMax]

# Plot -- Volume line graph
plt.figure(figsize=(9, 5))
plt.title(case, fontsize = 15, fontweight = "bold")
plt.xlabel("$Time$")
plt.ylabel("$Number\ of\ nodes$")
plt.axhline(y = max(amount) * 0.25, color='r', linestyle=':', alpha=0.8)
plt.axhline(y = amountAvg, color='g', linestyle=':', alpha=0.8)
plt.plot(unixTimestampPlot, amount, color='b', marker='.')
plt.plot(largestTime, max(amount), color='#FF5E13', marker='D')
plt.ylim(0, )
if len(dateTimeHalfYear) % 6 != 0:
    x_ticks = np.arange(min(unixTimestampXaxis), max(unixTimestampXaxis) + 15552000, 15552000)
elif len(dateTimeHalfYear) % 6 == 0:
    x_ticks = np.arange(min(unixTimestampXaxis), max(unixTimestampXaxis), 15552000)
plt.xticks(x_ticks, dateTimeHalfYear, rotation=30)
plt.tight_layout()
plt.show()

# Node (pending upgrade)
time, layer, relatedLink = [], [], []
authorZero, authorFirst, authorSecond, authorThird, authorForth, authorForthUp = "", "", "", "", "", ""
authorList = [authorZero, authorFirst, authorSecond, authorThird, authorForth, authorForthUp]
numList = [1, 2, 3, 4, 99]
print(authorList)
for i in data:
    conditionOne = i["type"] == "article"
    conditionTwo = int(i["time"]) < endTime
    conditionThree = i["article_id"] != i["parent_id"]
    if conditionOne and conditionTwo and conditionThree:
        time.append(str(i["time"]))    
    if conditionOne and conditionTwo and conditionThree and i["parent_id"] == "":
        layer.append(1)
        authorFirst += i["article_id"] + "\n"
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] in authorFirst:
        layer.append(2)
        authorSecond += i["article_id"] + "\n"
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] in authorSecond:
        layer.append(3)
        authorThird += i["article_id"] + "\n"
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] in authorThird:
        layer.append(4)
        authorForth += i["article_id"] + "\n"
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] in authorForth:
        layer.append(5)
        authorForthUp += i["article_id"] + "\n"
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] in authorForthUp:
        layer.append(6)
        author_sixth += i["article_id"] + "\n"
    else:
        pass
    
    if conditionOne and conditionTwo and conditionThree and i["related_link"] == "":
        relatedLink.append("")
    elif conditionOne and conditionTwo and conditionThree and i["related_link"].find("https://www.facebook.com/") != -1:
        relatedLink.append("")
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] != "" and i["related_link"].find("https://www.facebook.com/") == -1:
        relatedLink.append("")
    elif conditionOne and conditionTwo and conditionThree and i["parent_id"] == "" and i["related_link"].find("https://www.facebook.com/") == -1:
        relatedLink.append(i["related_link"])

# Related link time and layer
countList = []
for i in relatedLink:
    if i != '':
        countList.append(relatedLink.index(i))
        
# Related link to Layer 1 node
relatedTime, relatedLayer = [], []
layerOneLayer = []
for i in countList:
    relatedTime.append(int(time[i]))
    relatedLayer.append(0)
    layerOneLayer.append(1)

# Parse json 
pair = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < endTime and i["article_id"] != i["parent_id"]:
        pair += [[i["article_id"], str(i["time"]), i["parent_id"]]] #

# Add layer 
for x in range(len(layer)):
    pair[x] = pair[x] + [str(layer[x])]

# Article_id & parent_id relationship (pending upgrade)
pairs = []
for i in pair:
    if i[2] != "":
        for j in pair: # Layer 
            if i[2] == j[0] and j[0] == '':
                pairs += [[i[0], i[1], '1', i[2], j[1], '']] # 1. article_id, time, layer  2. parent_id, time, layer
            elif i[2] == j[0] and j[0] in authorFirst:
                pairs += [[i[0], i[1], '2', i[2], j[1], '1']]
            elif i[2] == j[0] and j[0] in authorSecond:
                pairs += [[i[0], i[1], '3', i[2], j[1], '2']]
            elif i[2] == j[0] and j[0] in authorThird:
                pairs += [[i[0], i[1], '4', i[2], j[1], '3']]
            elif i[2] == j[0] and j[0] in authorForth:
                pairs += [[i[0], i[1], '5', i[2], j[1], '4']]
            elif i[2] == j[0] and j[0] in authorForthUp:
                pairs += [[i[0], i[1], '6', i[2], j[1], '5']]
            else:
                pass

# Point (pending upgrade)
point1, point2 = [], []
for i in pairs:
    point1 += [[int(i[1]), int(i[2])]]
    point2 += [[int(i[4]), int(i[5])]]

point3, point4 = [], []
for i in zip(relatedTime, relatedLayer, layerOneLayer):
    point3 += [[i[0], i[1]]]
    point4 += [[i[0], i[2]]]

# Time to int 
time = [int(x) for x in time]

# Plot -- propagation graph
plt.figure(figsize=(9, 5))
y1, y2, y3, y4 = 1, 2, 3, 4
plt.xlabel("$Time$")
plt.ylabel("$Layer$")
plt.ylim(0, 4)
my_y_ticks = np.arange(0, 5, 1)
plt.yticks(my_y_ticks)
for i in range(5):
    plt.axhline(y=i, color='#B3B3B3', linestyle='-')
# plt.axvline(x=timestamp, color="green", linestyle=':') # Draw tfc check time line 
for i in range(len(point1)):
    x_values = [point1[i][0], point2[i][0]]
    y_values = [point1[i][1], point2[i][1]]
    plt.plot(x_values, y_values, color='red')
for i in range(len(point3)):
    x_values = [point3[i][0], point4[i][0]]
    y_values = [point3[i][1], point4[i][1]]
    plt.plot(x_values, y_values, color='green')
plt.plot(time, layer, 'b.')
plt.plot(relatedTime, relatedLayer, 'b.')
plt.title(case, fontsize=15, fontweight='bold')
if len(dateTimeHalfYear) % 6 != 0:
    x_ticks = np.arange(min(unixTimestampXaxis), max(unixTimestampXaxis) + 15552000, 15552000)
elif len(dateTimeHalfYear) % 6 == 0:
    x_ticks = np.arange(min(unixTimestampXaxis), max(unixTimestampXaxis), 15552000)
plt.xticks(x_ticks, dateTimeHalfYear, rotation=30)
plt.tight_layout()
plt.show()