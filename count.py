import json
import ssl
import urllib.request as request
import re
import matplotlib.pyplot as plt
import numpy as np
import caseList

fakeCase = []

for index in range(len(caseList.Fake_case_timestamp2)):
    num = caseList.Fake_case_20200928[index]
    case = "Case " + num

    # For SSL certificate
    ssl._create_default_https_context = ssl._create_unverified_context
    src = "https://raw.githubusercontent.com/ChiaYuSu/III/master/20200928/" + num + "/output.json"

    # Read json
    with request.urlopen(src) as response:
        data = json.load(response)
        
    data = sorted(data, key=lambda k: k['time'])

    # TFC timestamp
    tfc_timestamp = caseList.Fake_case_timestamp2[index]

    # Count node amount
    count = 0
    for i in data:
        if i["type"] == "article" and int(i["time"]) < tfc_timestamp:
            count += 1
    fakeCase.append(count)

print(fakeCase)