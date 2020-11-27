# coding=utf-8
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
import main
import configparser
from bs4 import BeautifulSoup
from datetime import datetime

# Input case
def inputcase():
    config = configparser.ConfigParser()
    config.sections()
    config.read('conf.ini')
    num = config['case']['num']
    case = "Case " + num
    
    return num, case

# # For SSL certificate
# def certificate():
#     num, _ = inputcase()
#     ssl._create_default_https_context = ssl._create_unverified_context
#     src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/" + num + "/case.json"
#     user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"

#     request = req.Request(src, headers={
#         "User-Agent": user_agent
#     })
    
#     return request

# # Read json (For URL)
# def data():
#     with req.urlopen(certificate()) as response:
#         data = json.load(response)
#     data = sorted(data, key=lambda k: k['time'])  # Json sorted by time
    
#     return data

# Read json
def data():
    num, _ = inputcase()
    with open('20200928\\' + num + '\\output.json', 'r', encoding = "utf-8") as json_file:
        data = json.load(json_file)
    data = sorted(data, key=lambda k: k['time'])  # Json sorted by time
    
    return data

def timetransfer(x):
    seconds_in_day = 60 * 60 * 24
    seconds_in_hour = 60 * 60
    seconds_in_minute = 60
    
    days = x // seconds_in_day
    hours = (x - (days * seconds_in_day)) // seconds_in_hour
    minutes = (x - (days * seconds_in_day) - (hours * seconds_in_hour)) // seconds_in_minute
    x = x - (days * seconds_in_day) - (hours * seconds_in_hour) - (minutes * seconds_in_minute)
    
    return days, hours, minutes, x

def timedata():
    # Find out the start and end time of the case
    time_list = []
    for i in data():
        if i["type"] == "article":
            time_list.append(str(i["time"]))
    start = int(str(min(time_list)))
    end = int(str(max(time_list)))

    # Unix Timestamp list for plot
    unixtime = []
    unixtime_count = int(((end - start) / 2592000) + 2)  # 86400 * 30 = 2592000
    for i in range(unixtime_count):
        unixtime.append(start + i * 2592000)

    # Format Unix Timestamp to DateTime
    datetime_month = []
    for i in unixtime:
        datetime_month.append(datetime.fromtimestamp(
            i).strftime('%Y-%m-%d %H:%M:%S'))
        
    # Calculate the number of nodes for each month
    amount, timeCount = [], []
    count = 0
    for i in range(unixtime_count - 1):
        for j in data():
            if j["type"] == "article" and int(j["time"]) >= unixtime[i] and int(j["time"]) <= unixtime[i+1]:
                count += 1
                timeCount.append(datetime.fromtimestamp(int(j["time"])).strftime('%Y-%m-%d'))
        amount.append(count)
        count = 0
    amount.append(0)

    # Amount bigger than 25% line
    amount_25, index_25, time_count_25 = [], [], []
    for i in amount:
        if i > max(amount) * 0.25 and len(datetime_month) > 1:
            amount_25.append(i)
            index_25.append(amount.index(i))
    for i in index_25:
        time_count_25.append(datetime_month[i][0:10])
    del time_count_25[0]

    # Average number of nodes per month
    amount_avg = sum(amount) / len(unixtime)
    
    return unixtime, unixtime_count, datetime_month, amount, amount_avg, amount_25, index_25, time_count_25

def relate():
    # Node (pending upgrade)
    time, layer, relatedLink = [], [], []
    authorFirst, authorSecond, authorThird, authorForth, authorForthUp = "", "", "", "", ""
    for i in data():
        conditionOne = i["type"] == "article"
        conditionTwo = i["article_id"] != i["parent_id"]
        if conditionOne and conditionTwo:
            time.append(str(i["time"]))
        if conditionOne and conditionTwo and i["parent_id"] == "":
            layer.append(1)
            authorFirst += i["article_id"] + "\n"
        elif conditionOne and conditionTwo and i["parent_id"] in authorFirst:
            layer.append(2)
            authorSecond += i["article_id"] + "\n"
        elif conditionOne and conditionTwo and i["parent_id"] in authorSecond:
            layer.append(3)
            authorThird += i["article_id"] + "\n"
        elif conditionOne and conditionTwo and i["parent_id"] in authorThird:
            layer.append(4)
            authorForth += i["article_id"] + "\n"
        elif conditionOne and conditionTwo and i["parent_id"] in authorForth:
            layer.append(5)
            authorForthUp += i["article_id"] + "\n"
        else:
            pass

        if conditionOne and conditionTwo and i["related_link"] == "":
            relatedLink.append("")
        elif conditionOne and conditionTwo and i["related_link"].find("https://www.facebook.com/") != -1:
            relatedLink.append("")
        elif conditionOne and conditionTwo and i["parent_id"] != "" and i["related_link"].find("https://www.facebook.com/") == -1:
            relatedLink.append("")
        elif conditionOne and conditionTwo and i["parent_id"] == "" and i["related_link"].find("https://www.facebook.com/") == -1:
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
    for i in data():
        if i["type"] == "article" and i["article_id"] != i["parent_id"]:
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
        point1 += [[datetime.fromtimestamp(int(i[1])).strftime('%Y-%m-%d %H:%M:%S'), int(i[2])]]
        # time + layer (article_id)
        point2 += [[datetime.fromtimestamp(int(i[4])).strftime('%Y-%m-%d %H:%M:%S'), int(i[5])]]

    # Point1 mix Point2
    node = []
    for i in range(len(point1)):
        node.append([point1[i], point2[i]])

    # Layer 0 (related_link)
    point3, point4 = [], []
    for i in zip(relatedTime, relatedLayer, layerOneLayer):
        # time + layer (related_link)
        point3 += [[datetime.fromtimestamp(int(i[0])).strftime('%Y-%m-%d %H:%M:%S'), int(i[1])]]
        # time + layer (layer 1 article_id)
        point4 += [[datetime.fromtimestamp(int(i[0])).strftime('%Y-%m-%d %H:%M:%S'), int(i[2])]]

    # Point3 mix Point4
    origin = []
    for i in range(len(point3)):
        origin.append([point3[i], point4[i]])
        
    return pairs, node, origin
    

def feature1():
    _, _, datetime_month, amount, amount_avg, _, _, _ = timedata()
    _, case = inputcase()
    # Feature 1 -- Volume
    quarter_line = 0
    for i in amount:
        if i > max(amount) * 0.25 and len(datetime_month) > 1:
            quarter_line += 1
    quarter_line -= 1

    # Plotly -- Volume line graph
    if len(datetime_month) > 1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=datetime_month,
            y=amount,
            mode='lines+markers',
            name="Volume line"
        ))
        fig.add_trace(go.Scatter(
            x=datetime_month,
            y=[max(amount)*0.25]*len(datetime_month),
            mode='lines',
            name="Critical line",
            marker=dict(color='rgba(255, 0, 0, 1)'),
        ))
        fig.add_trace(go.Scatter(
            x=datetime_month,
            y=[amount_avg]*len(datetime_month),
            mode='lines',
            name="Average line"
        ))
        star = amount.index(max(amount))
        starTime = datetime_month[star]
        fig.add_trace(go.Scatter(
            x=[starTime],
            y=[max(amount)],
            mode='markers',
            marker=dict(color='rgba(255, 127, 80, 1)', symbol='star', size=11),
            name="Base month"
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
    elif len(datetime_month) <= 1:
        pass
    f1 = quarter_line

    return f1, amount

# Feature 2 -- Time
def feature2():
    _, case = inputcase()
    pairs, node, origin = relate()
    def takethird(elem):
        return elem[3]

    articleID, parentID, articleTime, parentTime = [], [], [], []
    articleTime2, articleLayer2, parentTime2, parentLayer2, timeGap, timeGap2 = [], [], [], [], [], []
    f2 = 0
    feature2Pairs = pairs
    feature2Pairs.sort(key=takethird)
    for i in feature2Pairs:
        if int(i[3]) not in parentID:
            articleID, parentID, articleTime, parentTime = [], [], [], []
            articleID.append(int(i[0]))
            articleTime.append(int(i[1]))
            parentID.append(int(i[3]))
            parentTime.append(int(i[4]))
            if max(articleTime) - parentTime[0] > 259200 and (min(articleTime) - parentTime[0] < 259200) is False:
                f2 += 1
                articleTime2.append(datetime.fromtimestamp(
                    int(i[1])).strftime('%Y-%m-%d %H:%M:%S'))
                articleLayer2.append(int(i[2]))
                parentTime2.append(datetime.fromtimestamp(
                    int(i[4])).strftime('%Y-%m-%d %H:%M:%S'))
                parentLayer2.append(int(i[5]))
                timeGap.append(int(i[1])-int(i[4]))
        elif int(i[3]) in parentID:
            articleID.append(int(i[0]))
            articleTime.append(int(i[1]))
            parentID.append(int(i[3]))
            parentTime.append(int(i[4]))
            if max(articleTime) - parentTime[0] > 259200 and (min(articleTime) - parentTime[0] < 259200) is False:
                f2 += 1
                articleTime2.append(datetime.fromtimestamp(
                    int(i[1])).strftime('%Y-%m-%d %H:%M:%S'))
                articleLayer2.append(int(i[2]))
                parentTime2.append(datetime.fromtimestamp(
                    int(i[4])).strftime('%Y-%m-%d %H:%M:%S'))
                parentLayer2.append(int(i[5]))
                timeGap.append(int(i[1])-int(i[4]))

    for i in timeGap:
        seconds_in_day, seconds_in_hour, seconds_in_minute, x = timetransfer(i)
        timeGap2.append(str(seconds_in_day) + " days " + str(seconds_in_hour) + " hours " + str(seconds_in_minute) + " minutes " + str(x) + " seconds")

    # Plotly -- Propagation graph
    fig = go.Figure()
    for i in node:
        fig.add_trace(go.Scatter(
            x=(i[0][0], i[1][0]),
            y=(i[0][1], i[1][1]),
            mode='markers+lines',
            marker=dict(color='rgba(98, 110, 250, 1)'),
            name='Propagation'
        ))
        
    for i in origin:
        fig.add_trace(go.Scatter(
            x=(i[0][0], i[1][0]),
            y=(i[0][1], i[1][1]),
            mode='markers+lines',
            marker=dict(color='rgba(98, 110, 250, 1)'),
        ))
        
    for i in range(len(articleTime2)):
        fig.add_trace(go.Scatter(
            x=(articleTime2[i], parentTime2[i]),
            y=(articleLayer2[i], parentLayer2[i]),
            mode='markers+lines',
            marker=dict(color='rgba(255, 0, 0, 1)'),
            name='Time'
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
    fig.write_html(str(case) + "/feature2.html")
    
    return f2, articleTime2, articleLayer2, parentTime2, parentLayer2, timeGap, timeGap2

# Feature 3 -- Mainstream
def feature3():
    import time

    def googleScrape(searchList):
        urlQuery = []
        url = 'https://www.google.com.tw/search?q='
        user_agent = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36']
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
    query = data()[0]["body"].replace("\n", "")
    print(query)

    f3 = 0
    # official page url, title, related_link, fb old author_id, fb new author_id, fake list, comment with fakeWords
    tmp, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7 = 0, 0, 0, 0, 0, 0, 0
    fakeWords = ['tfc', 'TFC', '查核', '假的', '假新聞', 
                '謠言', '事實', '詐騙', '麥擱騙', 'MyGoPen', 
                'Cofacts', '【錯誤】', '駁斥', '網傳']
    for i in googleScrape([query]):
        for j in media.mainstream:
            if i.find(j) != -1:
                tmp += 1
        for k in media.fake:
            if i.find(k) != -1:
                tmp6 += 1
    for i in googleScrape2([query]):
        for j in fakeWords:
            if i.find(j) != -1:
                tmp2 += 1
    for i in data():
        if i["type"] == "article":
            for j in media.mainstream:
                if i["related_link"].find(j) != -1:
                    tmp3 += 1
            for k in media.mainstreamOldUID:
                if i["author_id"].find(k) != -1:
                    tmp4 += 1
            for l in media.mainstreamNewUID:
                if i["author_id"].find(l) != -1:
                    tmp5 += 1
        elif i["type"] == "comment":
            for m in fakeWords:
                if m in i["body"]:
                    tmp7 += 1
    f3 = tmp - tmp2 + tmp3 + tmp4 + tmp5 - tmp6 - tmp7
    
    return f3, query, tmp, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7

# Feature 4 -- Semantics
def feature4():
    fakeWords2 = ['請轉發', '請分享', '請告訴', '請注意', '請告知', 
                  '請轉告', '請廣發', '請傳給', '請大家轉告', '請分發', 
                  '告訴別人', '告訴家人', '告訴朋友', '把愛傳出去', '馬上發出去', 
                  '馬上發給', '已經上新聞', '相互轉發', '功德無量', '分享出去', 
                  '廣發分享', '緊急通知', '千萬不要', '千萬別', '緊急擴散', 
                  '重要訊息', '重要信息', '快轉發', '快分享', '快告訴',
                  '快告知', '快傳給', '快轉告', '擴散出去', '動動手指', 
                  '超級爆料', '請大家注意', '請大家轉發', '我的分享是真',
                 ]

    fakeWordsCount2 = [0] * len(fakeWords2)

    for i in data():
        for j in fakeWords2:
            if i["type"] == "article" and j in i["body"]:
                fakeWordsCount2[fakeWords2.index(j)] += 1
    f4 = sum(fakeWordsCount2)
    
    return f4, fakeWords2, fakeWordsCount2

# Feature 5 -- First comment time - first share time
def feature5():
    count_share = []
    count_comment = []
    share_comment_time = []
    for i in data():
        if i["type"] == "article":
            count_share.append(i["time"])
        elif i["type"] == "comment":
            count_comment.append(i["time"])
    if count_share != [] and count_comment != []:
        f5 = int(count_comment[0])-int(count_share[0])
        share_comment_time.append(datetime.fromtimestamp(
            int(count_share[0])).strftime('%Y-%m-%d %H:%M:%S'))
        share_comment_time.append(datetime.fromtimestamp(
            int(count_comment[0])).strftime('%Y-%m-%d %H:%M:%S'))
        seconds = int(count_comment[0])-int(count_share[0])
        # Convert seconds to days, hours, and minutes
        seconds_in_day, seconds_in_hour, seconds_in_minute, x = timetransfer(seconds)
        share_comment_time.append(str(seconds_in_day) + " days " + str(seconds_in_hour) + " hours " + str(seconds_in_minute) + " minutes " + str(x) + " seconds")
    elif count_share == []:
        f5 = 99999
        share_comment_time.append('No share')
        share_comment_time.append(datetime.fromtimestamp(
            int(count_comment[0])).strftime('%Y-%m-%d %H:%M:%S'))
        share_comment_time.append('-')
    elif count_comment == []:
        f5 = 99999
        share_comment_time.append(datetime.fromtimestamp(
            int(count_share[0])).strftime('%Y-%m-%d %H:%M:%S'))
        share_comment_time.append('No comment')
        share_comment_time.append('-')
    
    return f5, count_share, count_comment, share_comment_time
    

# Feature 6 -- Post and post time gap average
def feature6():
    timeList, postTime, timeListGap, timeListGap2 = [], [], [], []
    for i in data():
        timeList.append(int(i["time"]))
    for i in range(1, len(timeList)):
        gap = int(timeList[i]) - int(timeList[i-1])
        timeListGap2.append(gap)
        seconds_in_day, seconds_in_hour, seconds_in_minute, x = timetransfer(gap)
        timeListGap.append(str(seconds_in_day) + " days " + str(seconds_in_hour) + " hours " + str(seconds_in_minute) + " minutes " + str(x) + " seconds")
    for i in range(0, len(timeList)-1):
        postTime.append(datetime.fromtimestamp(int(timeList[i])).strftime('%Y-%m-%d %H:%M:%S') + " ~ " + datetime.fromtimestamp(int(timeList[i+1])).strftime('%Y-%m-%d %H:%M:%S'))
    average = sum(timeListGap2) // len(timeListGap2)
    f6 = average
    seconds_in_day, seconds_in_hour, seconds_in_minute, x = timetransfer(average)
    
    average = str(seconds_in_day) + " days " + str(seconds_in_hour) + " hours " + str(seconds_in_minute) + " minutes " + str(x) + " seconds"
    
    return f6, timeList, postTime, timeListGap, timeListGap2, average

# Feature 7 -- First node and the most popular node time gap
def feature7():
    pairs, _, _ = relate()
    _, count_share, _, _ = feature5()
    f7tmp = 0
    f7parentID, f7parentTime, f7count = [], [], []
    for i in pairs:
        if i[3] not in f7parentID:
            f7parentID.append(i[3])
            f7parentTime.append(i[4])
            
    for i in f7parentID:
        for j in pairs:
            if i == j[3]:
                f7tmp += 1
        f7count.append(f7tmp)
        f7tmp = 0
    maxOutdegree = f7count.index(max(f7count))
    f7gap = int(f7parentTime[maxOutdegree]) - int(count_share[0])
    f7 = f7gap
    seconds_in_day, seconds_in_hour, seconds_in_minute, x = timetransfer(f7gap)
    f7gap = str(seconds_in_day) + " days " + str(seconds_in_hour) + " hours " + str(seconds_in_minute) + " minutes " + str(x) + " seconds"
    f7parentTime[maxOutdegree] = datetime.fromtimestamp(int(f7parentTime[maxOutdegree])).strftime('%Y-%m-%d %H:%M:%S')
    count_share[0] = datetime.fromtimestamp(int(count_share[0])).strftime('%Y-%m-%d %H:%M:%S')
    f7time = [count_share[0], f7parentTime[maxOutdegree], f7gap]
    
    return f7, f7parentID, f7parentTime, f7count, f7time

# Real vs. Fake
def final_score():
    f1, _ = feature1()
    f2, _, _, _, _, _, _ = feature2()
    f3, _, _, _, _, _, _, _, _ = feature3()
    f4, _, _ = feature4()
    f5, _, _, _ = feature5()
    f6, _, _, _, _, _ = feature6()
    f7, _, _, _, _ = feature7()
    config = configparser.ConfigParser()
    config.sections()
    config.read('conf.ini')
    f1_score, f2_score, f3_score, f4_score, f5_score, f6_score, f7_score = 0, 0, 0, 0, 0, 0, 0
    score = 0
    if f1 > int(config['feature 1']['high_risk']):
        f1_score += 0
    elif f1 <= int(config['feature 1']['low_risk']):
        f1_score += 1
    if f2 > int(config['feature 2']['high_risk']):
        f2_score += 0
    elif f2 <= int(config['feature 2']['low_risk']):
        f2_score += 1
    if f3 >= int(config['feature 3']['low_risk']):
        f3_score += 1
    elif f3 >= int(config['feature 3']['middle_risk_1']) and f3 < int(config['feature 3']['middle_risk_2']):
        f3_score += 0.5
    elif f3 < int(config['feature 3']['high_risk']):
        f3_score += 0
    if f4 >= int(config['feature 4']['high_risk']):
        f4_score += 0
    elif f4 >= int(config['feature 4']['middle_risk_1']) and f4 < int(config['feature 4']['middle_risk_2']):
        f4_score += 0.5
    elif f4 >= int(config['feature 4']['low_risk_1']) and f4 < int(config['feature 4']['low_risk_2']):
        f4_score += 1
    if f5 <= int(config['feature 5']['low_risk']):
        f5_score += 1
    elif f5 > int(config['feature 5']['middle_risk_1']) and f5 <= int(config['feature 5']['middle_risk_2']):
        f5_score += 0.5
    elif f5 > int(config['feature 5']['high_risk']):
        f5_score += 0
    if f6 > int(config['feature 6']['high_risk']):
        f6_score += 0
    elif f6 >= int(config['feature 6']['middle_risk_1']) and f6 <= int(config['feature 6']['middle_risk_2']):
        f6_score += 0.5
    elif f6 < int(config['feature 6']['low_risk']):
        f6_score += 1
    if f7 >= int(config['feature 7']['high_risk']):
        f7_score += 0
    elif f7 == int(config['feature 7']['middle_risk']):
        f7_score += 0.5
    elif f7 < int(config['feature 7']['low_risk']):
        f7_score += 1
        
    score = f1_score * float(config['weight']['1']) + f2_score * float(config['weight']['2']) + f3_score * float(config['weight']['3']) + f4_score * float(config['weight']['4']) + f5_score * float(config['weight']['5']) + f6_score * float(config['weight']['6']) + f7_score * float(config['weight']['7'])

    score = round(score, 3)
    
    return score