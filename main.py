import json
import ssl
import urllib.request as request
ssl._create_default_https_context = ssl._create_unverified_context
src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/324/case.json"

def data():
    with request.urlopen(src) as response:
        result = ""
        data = json.load(response)
        for line in data:
            if line["author_id"] not in result and line["type"] == "article":
                result += ("https://facebook.com/" + line["author_id"] + "\n")
        return result
    
with open("data.txt", mode="w") as file:
    file.write(data())