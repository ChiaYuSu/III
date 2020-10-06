# Import modules
import json
import ssl
import urllib.request as request
import re
import matplotlib.pyplot as plt
import numpy as np

num = "Real39"
case = "Case " + num

# For SSL certificate
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200928/" + num + "/output.json"

# Read json
with request.urlopen(src) as response:
    data = json.load(response)
    
data = sorted(data, key=lambda k: k['time'])

# Write json to file
with open('case.json', mode='w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)

# TFC timestamp
timestamp = 1601438400
tfc_timestamp = int(str(1601438400)) #

# Get the smallest timestamp
lists = []
for i in data:
    if i["type"] == "article" and int(i["time"]) < tfc_timestamp:
        lists.append(str(i["time"]))
smallest = int(str(min(lists))) #
biggest = int(str(max(lists))) #

# Count
count = 0
for i in data:
    if i["type"] == "article" and int(i["time"]) > 1510000000 and int(i["time"]) < 1520000000:
        count += 1
print(count)

# Node
time, layer, related = [], [], []
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
    if i["type"] == "article" and i["related_link"] == "" and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]:
        related.append("")
    elif i["type"] == "article" and i["related_link"].find("https://www.facebook.com/") != -1 and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"]: # find facebook
        related.append("")
    elif i["type"] == "article" and i["related_link"].find("https://www.facebook.com/") == -1 and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"] and i["parent_id"] != "":
        related.append("")
    elif i["type"] == "article" and i["related_link"].find("https://www.facebook.com/") == -1 and int(i["time"]) < tfc_timestamp and i["article_id"] != i["parent_id"] and i["parent_id"] == "":
        related.append(i["related_link"])
        
# print(time)
print(layer)
# print(related)
# print(len(layer))
# print(len(related))

# Related link time and layer
countList = []
for i in related:
    if i != '':
        countList.append(related.index(i))
        
# Related link to Layer 1 node
relatedTime, relatedLayer = [], []
layerOneLayer = []
for i in countList:
    relatedTime.append(int(time[i]))
    relatedLayer.append(0)
    layerOneLayer.append(1)
# print(relatedTime)
# print(relatedLayer)

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

point3, point4 = [], []
for i in zip(relatedTime, relatedLayer, layerOneLayer):
    point3 += [[i[0], i[1]]]
    point4 += [[i[0], i[2]]]
# print(point3)
# print(point4)

# Time to int --------------------------------------------------------------->
time = [int(x) for x in time]

# Plot x:unix timestamp y:layer --------------------------------------------->
plt.figure(figsize=(9,6))
# x = np.linspace(smallest, tfc_timestamp, tfc_timestamp - smallest + 1)
y1, y2, y3, y4 = 1, 2, 3, 4
plt.xlabel("$Unix Timestamp$")
plt.ylabel("$Layer$")
# plt.xlim(smallest, smallest + 62208000) # 3 month = 7776000, 6 month = 15552000, 9 month = 23328000, 12 month = 31104000, 15 month = 38880000, 18 month = 46656000, 21 month = 54432000, 24 month = 62208000
# plt.ylim(0, 5)
my_y_ticks = np.arange(0, 5, 1)
plt.yticks(my_y_ticks)
for i in range(5):
    plt.axhline(y=i, color='#B3B3B3', linestyle='-')
plt.axvline(x=timestamp, color="#000000", linestyle='-')
for i in range(len(point1)):
    x_values = [point1[i][0], point2[i][0]]
    y_values = [point1[i][1], point2[i][1]]
    plt.plot(x_values, y_values, 'r')
for i in range(len(point3)):
    x_values = [point3[i][0], point4[i][0]]
    y_values = [point3[i][1], point4[i][1]]
    plt.plot(x_values, y_values, 'g')
plt.plot(time, layer, 'b.')
plt.plot(relatedTime, relatedLayer, 'b.')
plt.title(case, fontsize = 15, fontweight = "bold")
plt.show()

# Plot x:depth y:CCDF ------------------------------------------------------>
layerOneCCDF, layerTwoCCDF, layerThreeCCDF, layerFourCCDF, layerFiveCCDF, layerSixCCDF, layerSevenCCDF, layerEightCCDF, layerNineCCDF, layerTenCCDF, layerElevenCCDF = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0
plt.figure(figsize=(16,4))
for i in layer:
    if i >= 1:
        layerOneCCDF += 1
    if i >= 2:
        layerTwoCCDF += 1
    if i >= 3:
        layerThreeCCDF += 1
    if i >= 4:
        layerFourCCDF += 1
    if i >= 5:
        layerFiveCCDF += 1
    if i >= 6:
        layerSixCCDF += 1
    # if i >= 7:
    #     layerSevenCCDF += 1
    # if i >= 8:
    #     layerEightCCDF += 1 
    # if i >= 9:
    #     layerNineCCDF += 1
    # if i >= 10:
    #     layerTenCCDF += 1
        
CCDF1 = layerOneCCDF / len(layer)
CCDF2 = layerTwoCCDF / len(layer)
CCDF3 = layerThreeCCDF / len(layer) 
CCDF4 = layerFourCCDF / len(layer)
CCDF5 = layerFiveCCDF / len(layer)
CCDF6 = layerSixCCDF / len(layer)
# CCDF7 = layerSevenCCDF / len(layer)
# CCDF8 = layerEightCCDF / len(layer)
# CCDF9 = layerNineCCDF / len(layer)
# CCDF10 = layerTenCCDF / len(layer)

# print(CCDF1, CCDF2, CCDF3, CCDF4, CCDF5, CCDF6, CCDF7, CCDF8, CCDF9, CCDF10)

x_values = [x for x in range(1, 7)]
y_values = [CCDF1, CCDF2, CCDF3, CCDF4, CCDF5, CCDF6]

point5, point6 = [], []
for i in range(len(x_values)-1):
    point5 = [x_values[i], x_values[i+1]]
    point6 = [y_values[i], y_values[i+1]]
    plt.plot(point5, point6, 'b')

for i in range(len(x_values)):
    plt.plot(x_values[i], y_values[i], 'r.')
    
plt.xlim(1,)
plt.ylim(0, 1)
plt.xlabel("$Cascade$" + " " + "$Depth$")
plt.ylabel("$CCDF$")
plt.title(case, fontsize = 15, fontweight = "bold")
# plt.show()