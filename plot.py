# Import modules
import json
import ssl
import urllib.request as request
import re
import numpy as np
import statistics
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# Input case
num = "Real18"
case = "Case " + num

# For SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/" + num + "/case.json"

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
start = int(str(min(lists))) 
end = int(str(max(lists))) 

# Unix Timestamp list for plot (1 month)
unixTimestampPlot = []
stampCount = int(((end - start) / 2592000) + 1)  # 86400 * 30 = 2592000
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
    dateTimeMonth.append(datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S'))

# Format Unix Timestamp to DateTime (6 month)
dateTimeHalfYear = []
for i in unixTimestampXaxis:
    dateTimeHalfYear.append(datetime.utcfromtimestamp(i).strftime('%Y-%m-%d %H:%M:%S'))

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

# Feature 1 -- Volume
quarterLine = 0
for i in amount:
    if i > max(amount) * 0.25 and len(dateTimeHalfYear) > 1:
        quarterLine += 1
print("Feature 1:", quarterLine)    

# Plotly -- Volume line graph
if len(dateTimeHalfYear) > 1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dateTimeMonth,
        y=amount,
        mode='lines+markers',
        name="Volume of line graph"
    ))
    fig.add_trace(go.Scatter(
        x=dateTimeMonth,
        y=[max(amount)*0.25]*len(dateTimeMonth),
        mode='lines',
        name="25% line"
    ))
    fig.add_trace(go.Scatter(
        x=dateTimeMonth,
        y=[amountAvg]*len(dateTimeMonth),
        mode='lines',
        name="Average line"
    ))
    fig.update_layout(
        title=case,
        xaxis_title="$Time$",
        yaxis_title="$Number\ of\ nodes$"
    )
    fig.show()
elif len(dateTimeHalfYear) <= 1:
    pass

# Node (pending upgrade)
time, layer, relatedLink = [], [], []
authorZero, authorFirst, authorSecond, authorThird, authorForth, authorForthUp = "", "", "", "", "", ""
authorList = [authorZero, authorFirst, authorSecond, authorThird, authorForth, authorForthUp]
numList = [1, 2, 3, 4, 99]
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
        pair += [[i["article_id"], str(i["time"]), i["parent_id"]]]

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

# Layer 1 to 4
point1, point2 = [], []
for i in pairs:
    point1 += [[datetime.utcfromtimestamp(int(i[1])).strftime('%Y-%m-%d %H:%M:%S'), int(i[2])]]  # time + layer (parent_id)
    point2 += [[datetime.utcfromtimestamp(int(i[4])).strftime('%Y-%m-%d %H:%M:%S'), int(i[5])]]  # time + layer (article_id)

# Point1 mix Point2
node = []
for i in range(len(point1)):
    node.append([point1[i], point2[i]])

# Layer 0 (related_link)
point3, point4 = [], []
for i in zip(relatedTime, relatedLayer, layerOneLayer):
    point3 += [[datetime.utcfromtimestamp(int(i[0])).strftime('%Y-%m-%d %H:%M:%S'), int(i[1])]]  # time + layer (related_link)
    point4 += [[datetime.utcfromtimestamp(int(i[0])).strftime('%Y-%m-%d %H:%M:%S'), int(i[2])]]  # time + layer (layer 1 article_id)

# Point3 mix Point4
origin = []
for i in range(len(point3)):
    origin.append([point3[i], point4[i]])
    
# Feature 2 -- Time
def takeFifth(elem):
    return elem[4]
articleID, articleTime, parentTime = [], [], []
feature2, tmp, tmp2, tmp3, tmp4, tmp5 = 0, 0, 0, 0, 0, 0
feature2Pairs = pairs
feature2Pairs.sort(key=takeFifth)
for i in feature2Pairs:
    if int(i[3]) not in articleID:
        if parentTime != []:
            tmp = max(parentTime) - min(articleTime)
            tmp2 = min(parentTime) - min(articleTime)
        if (tmp2 < 259200) is False and tmp > 259200:
            feature2 += 1
        articleID, articleTime, parentTime = [], [], []
        articleID.append(int(i[3]))
        articleTime.append(int(i[4]))
        parentTime.append(int(i[1]))
        if i == -1:
            tmp3 = max(parentTime) - min(articleTime)
            if tmp3 > 259200:
                feature2 += 1
    elif int(i[3]) in articleID:
        parentTime.append(int(i[1]))
        if i == -1:
            tmp4 = max(parentTime) - min(articleTime)
            tmp5 = min(parentTime) - min(articleTime)
            if (tmp5 < 259200) is False and tmp4 > 259200:
                feature2 += 1
print("Feature 2:", feature2)


# Plotly -- Propagation graph
fig = go.Figure()
for i in node:
    fig.add_trace(go.Scatter(
        x=(i[0][0], i[1][0]),
        y=(i[0][1], i[1][1]),
        mode='markers+lines',
        marker=dict(color='rgba(98, 110, 250, 1)')
    ))

for i in origin:
    fig.add_trace(go.Scatter(
        x=(i[0][0], i[1][0]),
        y=(i[0][1], i[1][1]),
        mode='markers+lines',
        marker=dict(color='rgba(98, 110, 250, 1)')
    ))

fig.update_layout(
    title=case,
    xaxis_title="$Time$",
    yaxis_title="$Layer$",
    showlegend=False,
    yaxis=dict(
        tickmode='linear',
        tick0=1,
    )
)
fig.show()