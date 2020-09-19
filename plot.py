# Import modules
import json
import ssl
import urllib.request as request
import re
import matplotlib.pyplot as plt
import numpy as np
import pprint
import datetime as dt
import matplotlib.dates as mdates

num = "4167"
case = "Case " + num

# For SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200911/" + num + "/output.json"

# Read json
with request.urlopen(src) as response:
    data = json.load(response)
    
# Write json to file
# with open('case.json', mode='w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
    
# TFC timestamp
tfc_timestamp = int(str(1594872000)) #

# Get the smallest timestamp
lists = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp:
        lists.append(str(i["time"]))
smallest = int(str(min(lists))) #
biggest = int(str(max(lists))) #

# Node
time, layer = [], []
author_first, author_second, author_third, author_forth, author_fifth, author_sixth, author_seventh, author_eight, author_nine, author_ten = "", "", "", "", "", "", "", "", "", ""
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp:
        time.append(str(i["time"])) #
    if i["type"] == "article" and i["parent_id"] == "" and int(i["time"]) < tfc_timestamp:
        layer.append(1)
        author_first += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_first and int(i["time"]) < tfc_timestamp:
        layer.append(2)
        author_second += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_second and int(i["time"]) < tfc_timestamp:
        layer.append(3)
        author_third += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_third and int(i["time"]) < tfc_timestamp:
        layer.append(4)
        author_forth += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_forth and int(i["time"]) < tfc_timestamp:
        layer.append(5)
        author_fifth += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_fifth and int(i["time"]) < tfc_timestamp:
        layer.append(6)
        author_sixth += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_sixth and int(i["time"]) < tfc_timestamp:
        layer.append(7)
        author_seventh += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_seventh and int(i["time"]) < tfc_timestamp:
        layer.append(8)
        author_eight += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_eight and int(i["time"]) < tfc_timestamp:
        layer.append(9)
        author_nine += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_nine and int(i["time"]) < tfc_timestamp:
        layer.append(10)
        author_ten += i["article_id"] + "\n"
        
print(time)
print(layer)

# Parse json ---------------------------------------------------------------->
pair = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp:
        pair += [[i["article_id"], str(i["time"]), i["parent_id"]]] #
# print(pair)

# Add layer ----------------------------------------------------------------->
for x in range(len(layer)):
    pair[x] = pair[x] + [str(layer[x])]
# print(pair)

# Article_id & parent_id relationship --------------------------------------->
pairs = []
for i in pair:
    if i[2] != "":
        for j in pair: # Layer 
            if i[2] == j[0] and j[0] == '':
                pairs += [[i[0], i[1], '1', i[2], j[1], '']] # 1. article_id, time, layer  2. parent_id, time, layer
            elif i[2] == j[0] and j[0] in author_first:
                pairs += [[i[0], i[1], '2', i[2], j[1], '1']]
            elif i[2] == j[0] and j[0] in author_second:
                pairs += [[i[0], i[1], '3', i[2], j[1], '2']]
            elif i[2] == j[0] and j[0] in author_third:
                pairs += [[i[0], i[1], '4', i[2], j[1], '3']]
            # elif i[2] == j[0] and j[0] in author_forth:
            #     pairs += [[i[0], i[1], '5', i[2], j[1], '4']]
            # elif i[2] == j[0] and j[0] in author_fifth:
            #     pairs += [[i[0], i[1], '6', i[2], j[1], '5']]
# print(pairs)

# Point
point1, point2 = [], []
for i in pairs:
    point1 += [[int(i[1]), int(i[2])]]
    point2 += [[int(i[4]), int(i[5])]]
print(point1)
print(point2)

# Time to int --------------------------------------------------------------->
time = [int(x) for x in time]

# Plot ---------------------------------------------------------------------->
plt.figure(figsize=(9,6))
# x = np.linspace(smallest, tfc_timestamp, tfc_timestamp - smallest + 1)
y1, y2, y3, y4 = 1, 2, 3, 4
plt.xlabel("$Unix Timestamp$")
plt.ylabel("$Layer$")
# plt.xlim(smallest, biggest)
# plt.ylim(0, 5)
my_y_ticks = np.arange(0, 5, 1)
plt.yticks(my_y_ticks)
for i in range(5):
    plt.axhline(y=i, color='#B3B3B3', linestyle='-')
for i in range(len(point1)):
    x_values = [point1[i][0], point2[i][0]]
    y_values = [point1[i][1], point2[i][1]]
    plt.plot(x_values, y_values, 'r')
plt.plot(time, layer, 'b.')
plt.title(case, fontsize = 15, fontweight = "bold")
plt.show()