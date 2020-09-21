# Import modules
import json
import ssl
import urllib.request as request
import re
import matplotlib.pyplot as plt
import numpy as np
import pprint
import sys

num = "Real14"
case = "Case " + num

# For SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/" + num + "/case.json"

# Read json
with request.urlopen(src) as response:
    data = json.load(response)
    
data = sorted(data, key=lambda k: k['time'])

# Write json to file
with open('case.json', mode='w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# TFC timestamp
tfc_timestamp = int(str(1600488000)) #

# Get the smallest timestamp
lists = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp:
        lists.append(str(i["time"]))
smallest = int(str(min(lists))) #
biggest = int(str(max(lists))) #

# Node
time, layer = [], []
author_first, author_second, author_third, author_forth, author_fifth, author_sixth, author_seventh, author_eight, author_nine, author_ten, author_eleven, author_twelve, author_thirteen, author_fourteen, author_fifteen, author_sixteen, author_seventeen, author_eighteen, authot_nineteen = "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        time.append(str(i["time"])) #
    if i["type"] == "article" and i["parent_id"] == "" and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(1)
        author_first += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_first and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(2)
        author_second += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_second and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(3)
        author_third += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_third and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(4)
        author_forth += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_forth and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(5)
        author_fifth += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_fifth and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(6)
        author_sixth += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_sixth and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(7)
        author_seventh += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_seventh and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(8)
        author_eight += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_eight and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(9)
        author_nine += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_nine and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(10)
        author_ten += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_ten and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(11)
        author_eleven += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_eleven and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(12)
        author_twelve += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_twelve and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(13)
        author_thirteen += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_thirteen and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(14)
        author_fourteen += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_fourteen and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(15)
        author_fifteen += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_fifteen and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(16)
        author_sixteen += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_sixteen and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(17)
        author_seventeen += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_seventeen and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(18)
        author_eighteen += i["article_id"] + "\n"
    elif i["type"] == "article" and i["parent_id"] in author_eighteen and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        layer.append(19)
        author_nineteen += i["article_id"] + "\n"
    else:
        pass
        
print(time)
print(layer)

# Parse json ---------------------------------------------------------------->
pair = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
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
            elif i[2] == j[0] and j[0] in author_forth:
                pairs += [[i[0], i[1], '5', i[2], j[1], '4']]
            elif i[2] == j[0] and j[0] in author_fifth:
                pairs += [[i[0], i[1], '6', i[2], j[1], '5']]
            elif i[2] == j[0] and j[0] in author_sixth:
                pairs += [[i[0], i[1], '7', i[2], j[1], '6']]
            elif i[2] == j[0] and j[0] in author_seventh:
                pairs += [[i[0], i[1], '8', i[2], j[1], '7']]
            elif i[2] == j[0] and j[0] in author_eight:
                pairs += [[i[0], i[1], '9', i[2], j[1], '8']]
            elif i[2] == j[0] and j[0] in author_nine:
                pairs += [[i[0], i[1], '10', i[2], j[1], '9']]
            elif i[2] == j[0] and j[0] in author_ten:
                pairs += [[i[0], i[1], '11', i[2], j[1], '10']]
            elif i[2] == j[0] and j[0] in author_eleven:
                pairs += [[i[0], i[1], '12', i[2], j[1], '11']]
            elif i[2] == j[0] and j[0] in author_twelve:
                pairs += [[i[0], i[1], '13', i[2], j[1], '12']]
            elif i[2] == j[0] and j[0] in author_thirteen:
                pairs += [[i[0], i[1], '14', i[2], j[1], '13']]
            elif i[2] == j[0] and j[0] in author_fourteen:
                pairs += [[i[0], i[1], '15', i[2], j[1], '14']]
            elif i[2] == j[0] and j[0] in author_fifteen:
                pairs += [[i[0], i[1], '16', i[2], j[1], '15']]
            elif i[2] == j[0] and j[0] in author_sixteen:
                pairs += [[i[0], i[1], '17', i[2], j[1], '16']]
            elif i[2] == j[0] and j[0] in author_seventeen:
                pairs += [[i[0], i[1], '18', i[2], j[1], '17']]
# print(pairs)

# Point
point1, point2 = [], []
for i in pairs:
    point1 += [[int(i[1]), int(i[2])]]
    point2 += [[int(i[4]), int(i[5])]]
# print(point1)
# print(point2)

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
my_y_ticks = np.arange(0, 18, 1)
plt.yticks(my_y_ticks)
for i in range(18):
    plt.axhline(y=i, color='#B3B3B3', linestyle='-')
for i in range(len(point1)):
    x_values = [point1[i][0], point2[i][0]]
    y_values = [point1[i][1], point2[i][1]]
    plt.plot(x_values, y_values, 'r')
plt.plot(time, layer, 'b.')
plt.title(case, fontsize = 15, fontweight = "bold")
plt.show()