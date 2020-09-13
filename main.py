import json
import ssl
import random
import urllib.request as request
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200911/case.json"
timestamp = 1595347200


class Crawler:
    def __init__(self):
        with request.urlopen(src) as response:
            self.result = ""
            data = json.load(response)

            for line in data:
                line["time"] = int(line["time"])

            for line in data:
                if line["type"] == "article" and line["parent_id"] != "" and line["time"] < timestamp:
                    self.result += (line["author_id"] + "\n")
                
            # string to list
            self.result_list = self.result.split("\n")

            # author_id >= 2
            self.repeat = ""
            for i in self.result_list:
                if self.result_list.count(i) >= 2:
                    if i not in self.repeat:
                        self.repeat += i + "\n"
            self.repeat = self.repeat.split("\n")

            # raw-data == repeat-data
            self.final = ""
            for i in data:
                if i["author_id"] in self.repeat and i["type"] == "article" and i["parent_id"] != "":
                    self.final += ("author_id: " + i["author_id"] + ", " + "parent_id: " + i["parent_id"]) + "\n"
            self.final = self.final.split("\n")
            self.final = set(self.final)
            self.final = sorted(self.final)

            # remove unique data
            for i in range(len(self.final)):
                # print(self.final[i])
                pass
                
            
            
            # sort
            self.sort = ""
            for i in self.final:
                self.sort += i + "\n"
            
t = Crawler()
with open("data.txt", mode="w") as file:
    file.write(t.sort)