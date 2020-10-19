# Import modules
import json
import ssl
import urllib.request as req
import re
import numpy as np
import statistics
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import random
import sys
import requests
import media
import os
from bs4 import BeautifulSoup
from urllib.parse import unquote
from datetime import datetime

# Input case
num = "559"
case = "Case " + num

# For SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/" + \
    num + "/case.json"

request = req.Request(src, headers={
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
})

# TFC timestamp
timestamp = 1601308800  # Draw tfc check time line
endTime = int(str(1602475200))  # Adjust case end timestamp

# Read json
with req.urlopen(request) as response:
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
stampCount = int(((end - start) / 2592000) + 2)  # 86400 * 30 = 2592000
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
    dateTimeMonth.append(datetime.utcfromtimestamp(
        i).strftime('%Y-%m-%d %H:%M:%S'))

# Format Unix Timestamp to DateTime (6 month)
dateTimeHalfYear = []
for i in unixTimestampXaxis:
    dateTimeHalfYear.append(datetime.utcfromtimestamp(
        i).strftime('%Y-%m-%d %H:%M:%S'))

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
    if i > max(amount) * 0.25 and len(dateTimeMonth) > 1:
        quarterLine += 1
quarterLine -= 1
print("Feature 1:", quarterLine)

# Plotly -- Volume line graph
if len(dateTimeMonth) > 1:
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
        xaxis_title="Time",
        yaxis_title="Number of nodes",
        margin=go.layout.Margin(
            l=0,  # left margin
            r=0,  # right margin
            b=0,  # bottom margin
            t=0  # top margin
        ),
        legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
)
    )
    # Write to HTML
    if not os.path.exists(str(case)):
        os.mkdir(str(case))
    fig.write_html(str(case) + "/feature1.html")
elif len(dateTimeMonth) <= 1:
    pass


# Node (pending upgrade)
time, layer, relatedLink = [], [], []
authorZero, authorFirst, authorSecond, authorThird, authorForth, authorForthUp = "", "", "", "", "", ""
authorList = [authorZero, authorFirst, authorSecond,
              authorThird, authorForth, authorForthUp]
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
        for j in pair:  # Layer
            if i[2] == j[0] and j[0] == '':
                # 1. article_id, time, layer  2. parent_id, time, layer
                pairs += [[i[0], i[1], '1', i[2], j[1], '']]
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
    # time + layer (parent_id)
    point1 += [[datetime.utcfromtimestamp(int(i[1])
                                          ).strftime('%Y-%m-%d %H:%M:%S'), int(i[2])]]
    # time + layer (article_id)
    point2 += [[datetime.utcfromtimestamp(int(i[4])
                                          ).strftime('%Y-%m-%d %H:%M:%S'), int(i[5])]]

# Point1 mix Point2
node = []
for i in range(len(point1)):
    node.append([point1[i], point2[i]])

# Layer 0 (related_link)
point3, point4 = [], []
for i in zip(relatedTime, relatedLayer, layerOneLayer):
    # time + layer (related_link)
    point3 += [[datetime.utcfromtimestamp(int(i[0])
                                          ).strftime('%Y-%m-%d %H:%M:%S'), int(i[1])]]
    # time + layer (layer 1 article_id)
    point4 += [[datetime.utcfromtimestamp(int(i[0])
                                          ).strftime('%Y-%m-%d %H:%M:%S'), int(i[2])]]

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
    xaxis_title="Time",
    yaxis_title="Layer",
    showlegend=False,
    yaxis=dict(
        tickmode='linear',
        tick0=1,
    ),
    margin=go.layout.Margin(
        l=0,  # left margin
        r=0,  # right margin
        b=0,  # bottom margin
        t=0  # top margin
    )
)

# Write to HTML
if not os.path.exists(str(case)):
    os.mkdir(str(case))
fig.write_html(str(case) + "/feature2.html")

# Feature 3 -- Mainstream
import time

def googleScrape(searchList):
    urlQuery = []
    url = 'https://www.google.com.tw/search?q='
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36']
    headers = {'User-Agent': user_agent[0]}
    for p in range(0, 30, 10):
        for i in searchList:
            time.sleep(1)
            res = requests.get(url=url+i+"&start="+str(p), headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            searchText = soup.find_all("div", class_="g")
            for j in searchText:
                urlQuery.append(j.find("a").get('href'))
    return urlQuery


def googleScrape2(searchList):
    titleQuery = []
    url = 'https://www.google.com.tw/search?q='
    user_agent = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36']
    headers = {'User-Agent': user_agent[0]}
    for p in range(0, 30, 10):
        for i in searchList:
            time.sleep(1)
            res = requests.get(url=url+i+"&start="+str(p), headers=headers)
            soup = BeautifulSoup(res.text, "html.parser")
            searchText = soup.find_all("div", class_="g")
            for j in searchText:
                titleQuery.append(j.find("a").text)
    return titleQuery


# Mainstream count
data = sorted(data, key=lambda k: k['time'])
query = data[0]["body"].replace("\n", "")
print(query)

feature3 = 0
tmp, tmp2, tmp3, tmp4, tmp5 = 0, 0, 0, 0, 0  # official page url, title, related_link, fb old author_id, fb new author_id
for i in googleScrape([query]):
    for j in media.mainstream:
        if i.find(j) != -1:
            tmp += 1
for i in googleScrape2([query]):
    for j in ['tfc', 'TFC', '查核', '假的', '假新聞', '謠言', '事實', '詐騙', '麥擱騙', "MyGoPen", "Cofacts"]:
        if i.find(j) != -1:
            tmp2 += 1
for i in data:
    for j in media.mainstream:
        if i["related_link"].find(j) != -1:
            tmp3 += 1
    for k in media.mainstreamOldUID:
        if i["author_id"].find(k) != -1:
            tmp4 += 1
    for l in media.mainstreamNewUID:
        if i["author_id"].find(l) != -1:
            tmp5 += 1
feature3 = tmp - tmp2 + tmp3 + tmp4 + tmp5
print("Feature 3:", feature3)

# Feature 4 -- Semantics
fakeWords = ['請轉發', '請分享', '請告訴', '請注意', '請告知', '請轉告', '請廣發', 
             '請傳給', '請大家轉告', '請分發', '告訴別人', '告訴家人', '告訴朋友', 
             '把愛傳出去', '馬上發出去', '馬上發給', '已經上新聞', '相互轉發', 
             '功德無量', '分享出去', '廣發分享', '緊急通知', '千萬不要', '千萬別', 
             '緊急擴散', '重要訊息', '重要信息', '快轉發', '快分享', '快告訴',
             '快告知', '快傳給', '快轉告']

fakeWordsCount = [0] * len(fakeWords)

for i in data:
    for j in fakeWords:
        if i["type"] == "article" and j in i["body"]:
            fakeWordsCount[fakeWords.index(j)] += 1
feature4 = sum(fakeWordsCount)
print("Feature 4:", feature4)

# Real vs. Fake
score = 0
if quarterLine > 0:
    score += 0
elif quarterLine <= 0:
    score += 1
if feature2 > 0:
    score += 0
elif feature2 <= 0:
    score += 1
if feature3 >= 4:
    score += 1
elif feature3 >= 0 and feature3 < 4:
    score += 0.5
elif feature3 < 0:
    score += 0
if feature4 >= 10:
    score += 0
elif feature4 >= 3 and feature4 < 10:
    score += 0.5
elif feature4 >= 0 and feature4 < 3:
    score += 1

print(score)
