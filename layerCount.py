import json
import ssl
import random
import urllib.request as request
import re

ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/454/case.json"

with request.urlopen(src) as response:
    data = json.load(response)

count_article = 0
count_first = 0
count_second = 0
count_third = 0
count_forth = 0
timestamp = 1588910400

for line in data:
    line["time"] = int(line["time"])
    if line["type"] == "article" and line["time"] < timestamp:
        count_article += 1

# layer 1 (post) ------------------------------------------------------------------------------------------------------->
author_first = ""
for line in data:
    if line["type"] == "article" and line["parent_id"] == "" and line["time"] < timestamp:
        count_first += 1
        author_first += line["article_id"] + "\n"

# string to list, del empty string
author_first = author_first.split("\n")
del(author_first[-1])

# layer 1 (post) ------------------------------------------------------------------------------------------------------->

# layer 2 (share 1) ---------------------------------------------------------------------------------------------------->
author_second = ""
for line in data:
    if line["type"] == "article" and line["parent_id"] in author_first and line["time"] < timestamp:
        author_second += line["article_id"] + "\n"
        count_second += 1

# string to list, del empty string
author_second = author_second.split("\n")
del(author_second[-1])

# layer 2 (share 1) ---------------------------------------------------------------------------------------------------->

# layer 3 (share 2) ---------------------------------------------------------------------------------------------------->
author_third = ""
for line in data:
    if line["type"] == "article" and line["parent_id"] in author_second and line["time"] < timestamp:
        author_third += line["article_id"] + "\n"
        count_third += 1

# string to list, del empty string
author_third = author_third.split("\n")
del(author_third[-1])

# layer 3 (share 2) ---------------------------------------------------------------------------------------------------->

# layer 4 (share 3) ---------------------------------------------------------------------------------------------------->
author_forth = ""
for line in data:
    if line["type"] == "article" and line["parent_id"] in author_third and line["time"] < timestamp:
        author_forth += line["article_id"] + "\n"
        count_forth += 1

# string to list, del empty string
author_forth = author_forth.split("\n")
del(author_forth[-1])

# layer 4 (share 3) ---------------------------------------------------------------------------------------------------->

count_forth_up = count_article - count_first - count_second - count_third - count_forth

# percent -------------------------------------------------------------------------------------------------------------->
percent_first = count_first / count_article
percent_second = count_second / count_article
percent_third = count_third / count_article
percent_forth = count_forth / count_article
percent_forth_up = count_forth_up / count_article
# percent -------------------------------------------------------------------------------------------------------------->

# print
print("Layer 1 :", count_first, "({0:.2%})".format(percent_first))
print("Layer 2 :", count_second, "({0:.2%})".format(percent_second))
print("Layer 3 :", count_third, "({0:.2%})".format(percent_third))
print("Layer 4 :", count_forth, "({0:.2%})".format(percent_forth))
print("Later 4↑:", count_forth_up, "({0:.2%})".format(percent_forth_up))
print("count_article:", count_article)

class Account:
    def __init__(self):
        self.first = "Layer 1:" + "\n"
        self.second = "Layer 2:" + "\n"
        self.third = "Layer 3:" + "\n"
        self.forth = "Layer 4:" + "\n"
        for i in author_first:
            self.first += "https://www.facebook.com/" + i + "\n"
        for i in author_second:
            self.second += "https://www.facebook.com/" + i + "\n"
        for i in author_third:
            self.third += "https://www.facebook.com/" + i + "\n" 
        for i in author_forth:
            self.forth += "https://www.facebook.com/" + i + "\n"
        self.result = self.first + "\n" + self.second + "\n" + self.third + "\n" + self.forth
        
        print("Layer 1 article_id:", author_first)
        print("---------------------------------------------------------------------------------")
        print("Layer 2 article_id:", author_second)
        print("---------------------------------------------------------------------------------")
        print("Layer 3 article_id:", author_third)
        print("---------------------------------------------------------------------------------")
        print("Layer 4 article_id:", author_forth)

t = Account()
with open("fb_account.txt", mode='w') as file:
    file.write(t.result)