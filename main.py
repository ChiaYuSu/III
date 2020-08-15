import json
import ssl
import urllib.request as request
ssl._create_default_https_context = ssl._create_unverified_context

def data():
    src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200702/articles_662/case.json"
    result = ""
    with request.urlopen(src) as responese:
        data = json.load(responese)
        for i in data:
            if i["author_id"] not in result:
                result += ("https://facebook.com/" + i["author_id"] + "\n")
        return result

with open("data.txt", mode="w") as file:
    file.write(data())