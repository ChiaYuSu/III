import json
import ssl
import random
import urllib.request as request
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/513/case.json"

class Crawler:
    def __init__(self):
        with request.urlopen(src) as response:
            self.result = ""
            self.count = 0
            data = json.load(response)
            for line in data:
                if line["author_id"] not in self.result and line["layer"] == 1:
                    self.result += ("https://facebook.com/" + line["author_id"] + "\n")
                    self.count = self.count + 1
            if self.count >= 30:
                self.result_list = str(self.result).split("\n")
                self.test = list(random.randint(1, self.count) for i in range(30))
                self.result = ""
                for i in self.test:
                    self.result += self.result_list[i] + "\n"
                self.test = str(self.test)

t = Crawler()
with open("data.txt", mode="w") as file:
    file.write(t.result)
    file.write(t.test)