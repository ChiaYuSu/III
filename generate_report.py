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
import codecs as co
import markdown
import plot
from pathlib import Path
from bs4 import BeautifulSoup
from datetime import datetime

# Case
def report():
    # import plot.py function
    _, case = plot.inputcase()
    _, _, datetime_month, amount, _, _, _, time_count_25 = plot.timedata()
    f1, amount = plot.feature1()
    f2, articleTime2, _, parentTime2, _, _, timeGap2 = plot.feature2()
    f3, query, tmp, tmp2, tmp3, tmp4, tmp5, tmp6, tmp7 = plot.feature3()
    f4, fakeWords2, fakeWordsCount2 = plot.feature4()
    f5, _, _, share_comment_time = plot.feature5()
    f6, _, postTime, timeListGap, _, average = plot.feature6()
    f7, _, _, _, f7time = plot.feature7()
    
    case = case
    caseName = query

    feature1 = case + "\\feature1.html"
    dateTime = []
    for i in datetime_month:
        dateTime.append(i[0:10])
    f1_1 = {'Month': dateTime, 'Quantity': amount}
    quantity1 = pd.DataFrame(f1_1)
    quantity1 = quantity1[~(quantity1 == 0).any(axis=1)]
    quantity1 = quantity1.sort_values(by=['Quantity'], ascending=False)
    f1_2 = {'Month': 'Total', 'Quantity': sum(amount)}
    quantity1 = quantity1.append(f1_2, ignore_index=True).set_index('Month')
    quantity1 = quantity1.to_markdown()

    count = 0
    if f1 > 0:
        cfbg1 = "F8D7DA"
        cfft1 = "721C24"
        cfhr1 = "F1B0B7"
        rf1_1 = "High"
        rf1_2 = "高"
        time = ""
        count = 0
        for i in time_count_25:
            if len(time_count_25) == 1:
                time += i
            else:
                if count == len(time_count_25)-1:
                    time = time[:-1]
                    time +=  " 與 " + i
                elif count != len(time_count_25)-1:
                    time += i + "、"
                    count += 1
        cf1 = case + " 在 " + time + " 高於 Critical line，所以針對此輸出結果，將特徵 1 判斷為高風險。"
    elif f1 == 0:
        cfbg1 = "D4EDDA"
        cfft1 = "155724"
        cfhr1 = "B1DFBB"
        rf1_1 = "Low"
        rf1_2 = "低"
        cf1 = case + " 皆沒有任何一點高於 Critical line，所以針對此輸出結果，將特徵 1 判斷為低風險。"

    feature2_1 = case + "\\feature2.html"
    f2_1= {"Original date": parentTime2, 'Later date': articleTime2, 'Time gap': timeGap2}
    feature2_2 = pd.DataFrame(f2_1)
    feature2_2 = feature2_2.set_index('Original date').sort_values(by=['Original date'])
    feature2_2 = feature2_2.to_markdown()

    if f2 > 0:
        cfbg2 = "F8D7DA"
        cfft2 = "721C24"
        cfhr2 = "F1B0B7"
        rf2_1 = "High"
        rf2_2 = "高"
        cf2 = case + " 在上述列表中曾出現過時間跨度大的現象，所以針對此輸出結果，將特徵 2 判斷為高風險。"
    elif f2 == 0:
        cfbg2 = "D4EDDA"
        cfft2 = "155724"
        cfhr2 = "B1DFBB"
        rf2_1 = "Low"
        rf2_2 = "低"
        cf2 = case + " 在上述列表中未曾出現過時間跨度大的現象，所以針對此輸出結果，將特徵 2 判斷為低風險。"

    f3_1 = {'Match URL': tmp, 'Match `related_link`': tmp3,
        'Match `author_id`': tmp4 + tmp5}
    quantity3_1 = pd.Series(f3_1)
    quantity3_1 = quantity3_1.rename('Quantity')
    feature3_1 = quantity3_1.to_markdown()
    f3_2 = {'Match URL': tmp2,
            'Match `body` of the article': tmp6,
            'Match `body` of the comment': tmp7}
    quantity3_2 = pd.Series(f3_2)
    quantity3_2 = quantity3_2.rename('Quantity')
    feature3_2 = quantity3_2.to_markdown()

    white = tmp + tmp3 + tmp4 + tmp5
    black = tmp2 + tmp6 + tmp7
    if f3 < 0:
        cfbg3 = "F8D7DA"
        cfft3 = "721C24"
        cfhr3 = "F1B0B7"
        rf3_1 = "High"
        rf3_2 = "高"
        cf3 = case + " 由於安全因素 (" + str(white) + ") - 風險因素 (" + str(black) + ") < 0，所以針對此輸出結果，將特徵 3 判斷為高風險。"
    elif f3 >= 0 and f3 < 4:
        cfbg3 = "FFF3CD"
        cfft3 = "856404"
        cfhr3 = "FFE8A1"
        rf3_1 = "Median"
        rf3_2 = "中"
        cf3 = case + " 由於安全因素 (" + str(white) + ") - 風險因素 (" + str(black) + ") 介於 0 到 4 之間，所以針對此輸出結果，將特徵 3 判斷為中風險。"
    elif f3 >= 4:
        cfbg3 = "D4EDDA"
        cfft3 = "155724"
        cfhr3 = "B1DFBB"
        rf3_1 = "Low"
        rf3_2 = "低"
        cf3 = case + " 由於安全因素 (" + str(white) + ") - 風險因素 (" + str(black) + ") ≥ 4，所以針對此輸出結果，將特徵 3 判斷為低風險。"

    f4_1 = {'Content': fakeWords2, 'Quantity': fakeWordsCount2}
    feature4_1 = pd.DataFrame(f4_1)
    feature4_1 = feature4_1[~(feature4_1 == 0).any(axis=1)]
    feature4_1 = feature4_1.sort_values(by=['Quantity'], ascending=False)
    f4_2 = {'Content': 'Total', 'Quantity': sum(fakeWordsCount2)}
    feature4_1 = feature4_1.append(f4_2, ignore_index=True).set_index('Content')
    feature4_1 = feature4_1.to_markdown()

    if f4 >= 10:
        cfbg4 = "F8D7DA"
        cfft4 = "721C24"
        cfhr4 = "F1B0B7"
        rf4_1 = "High"
        rf4_2 = "高"
        cf4 = case + " 在分享內文中出現過 ≥ 10 次的高風險字詞，所以針對此輸出結果，將特徵 4 判斷為高風險。"
    elif f4 >= 3 and f4 < 10:
        cfbg4 = "FFF3CD"
        cfft4 = "856404"
        cfhr4 = "FFE8A1"
        rf4_1 = "Median"
        rf4_2 = "中"
        cf4 = case + " 在分享內文中出現過介於 3 到 10 次的高風險字詞，所以針對此輸出結果，將特徵 4 判斷為中風險。"
    elif f4 >= 0 and f4 < 3:
        cfbg4 = "D4EDDA"
        cfft4 = "155724"
        cfhr4 = "B1DFBB"
        rf4_1 = "Low"
        rf4_2 = "低"
        cf4 = case + " 在分享內文中出現過介於 0 到 3 次的高風險字詞，所以針對此輸出結果，將特徵 4 判斷為低風險。"

    f5_1 = {'Type': ['First share time', 'First comment time', 'Time gap'], 'Time': share_comment_time}
    feature5_1 = pd.DataFrame(f5_1).set_index('Type')
    feature5_1 = feature5_1.to_markdown()

    if f5 > 3600:
        cfbg5 = "F8D7DA"
        cfft5 = "721C24"
        cfhr5 = "F1B0B7"
        rf5_1 = "High"
        rf5_2 = "高"
        cf5 = case + " 第一則留言與第一則分享時間差 > 60 分鐘，所以針對此輸出結果，將特徵 5 判斷為高風險。"
    elif f5 > 1800 and f5 <= 3600:
        cfbg5 = "FFF3CD"
        cfft5 = "856404"
        cfhr5 = "FFE8A1"
        rf5_1 = "Median"
        rf5_2 = "中"
        cf5 = case + " 第一則留言與第一則分享時間差介於 30 分鐘至 60 分鐘，所以針對此輸出結果，將特徵 5 判斷為中風險。"
    elif f5 <= 1800:
        cfbg5 = "D4EDDA"
        cfft5 = "155724"
        cfhr5 = "B1DFBB"
        rf5_1 = "Low"
        rf5_2 = "低"
        cf5 = case + " 第一則留言與第一則分享時間差 ≤ 30 分鐘，所以針對此輸出結果，將特徵 5 判斷為低風險。"

    f6_1 = {'Date': postTime, 'Time Gap': timeListGap}
    feature6_1 = pd.DataFrame(f6_1)
    f6_2 = {'Date': 'Average', 'Time Gap': average}
    feature6_1 = feature6_1.append(f6_2, ignore_index=True)
    feature6_1 = feature6_1[~(feature6_1 == 0).any(axis=1)].set_index('Date')
    feature6_1 = feature6_1.to_markdown()

    if f6 > 18000:
        cfbg6 = "F8D7DA"
        cfft6 = "721C24"
        cfhr6 = "F1B0B7"
        rf6_1 = "High"
        rf6_2 = "高"
        cf6 = case + " 兩貼文之間時間差 > 5 小時，所以針對此輸出結果，將特徵 6 判斷為高風險。"
    elif f6 >= 7200 and f6 <= 18000:
        cfbg6 = "FFF3CD"
        cfft6 = "856404"
        cfhr6 = "FFE8A1"
        rf6_1 = "Median"
        rf6_2 = "中"
        cf6 = case + " 兩貼文之間時間差介於 2 小時到 5 小時之間，所以針對此輸出結果，將特徵 6 判斷為中風險。"
    elif f6 < 7200:
        cfbg6 = "D4EDDA"
        cfft6 = "155724"
        cfhr6 = "B1DFBB"
        rf6_1 = "Low"
        rf6_2 = "低"
        cf6 = case + " 兩貼文之間時間差 < 2 小時，所以針對此輸出結果，將特徵 6 判斷為低風險。"
        
    f7_1 = {'Type': ['First share time', 'The most popular node time',
                'Time gap'], 'Time': f7time}
    feature7_1 = pd.DataFrame(f7_1).set_index('Type')
    feature7_1 = feature7_1.to_markdown()

    if f7 >= 108000:
        cfbg7 = "F8D7DA"
        cfft7 = "721C24"
        cfhr7 = "F1B0B7"
        rf7_1 = "High"
        rf7_2 = "高"
        cf7 = case + " 兩貼文之間時間差 > 30 小時，所以針對此輸出結果，將特徵 7 判斷為高風險。"
    elif f7 == 0:
        cfbg7 = "FFF3CD"
        cfft7 = "856404"
        cfhr7 = "FFE8A1"
        rf7_1 = "Median"
        rf7_2 = "中"
        cf7 = case + " 兩貼文之間時間差為 0，所以針對此輸出結果，將特徵 7 判斷為中風險。"
    elif f7 < 108000:
        cfbg7 = "D4EDDA"
        cfft7 = "155724"
        cfhr7 = "B1DFBB"
        rf7_1 = "Low"
        rf7_2 = "低"
        cf7 = case + " 兩貼文之間時間差 < 30 小時，所以針對此輸出結果，將特徵 7 判斷為低風險。"
        
    case2 = case
    risk = "{低/中/高}"

    md_template = open(r'markdown_template.md', encoding='utf8').read()
    md = md_template.format(case=case, caseName=caseName, feature1=feature1, quantity1=quantity1,
                            cfbg1=cfbg1, cfft1=cfft1, rf1_1=rf1_1, cf1=cf1, cfhr1=cfhr1, rf1_2=rf1_2,
                            feature2_1=feature2_1, feature2_2=feature2_2, 
                            cfbg2=cfbg2, cfft2=cfft2, rf2_1=rf2_1, cf2=cf2, cfhr2=cfhr2, rf2_2=rf2_2,
                            feature3_1=feature3_1, feature3_2=feature3_2,
                            cfbg3=cfbg3, cfft3=cfft3, rf3_1=rf3_1, cf3=cf3, cfhr3=cfhr3, rf3_2=rf3_2,
                            feature4_1=feature4_1, 
                            cfbg4=cfbg4, cfft4=cfft4, rf4_1=rf4_1, cf4=cf4, cfhr4=cfhr4, rf4_2=rf4_2,
                            feature5_1=feature5_1, 
                            cfbg5=cfbg5, cfft5=cfft5, rf5_1=rf5_1, cf5=cf5, cfhr5=cfhr5, rf5_2=rf5_2,
                            feature6_1=feature6_1,
                            cfbg6=cfbg6, cfft6=cfft6, rf6_1=rf6_1, cf6=cf6, cfhr6=cfhr6, rf6_2=rf6_2,
                            feature7_1=feature7_1,
                            cfbg7=cfbg7, cfft7=cfft7, rf7_1=rf7_1, cf7=cf7, cfhr7=cfhr7, rf7_2=rf7_2,
                            case2=case2, risk=risk)
    html_template = open(r'html_template.html', encoding='utf8').read()
    extensions = ['extra', 'smarty']
    html = markdown.markdown(md, extensions=extensions, output_format='html5')
    doc = html_template.replace('{{content}}', html)
    doc = doc.replace(
        '<table>', '<table class="table table-bordered table-striped">')
    doc = doc.replace('<img', '<img class="thumbnail img-responsive"')

    # Save report
    report = case + ".html"
    with open(report, 'w', encoding='utf-8') as f:
        f.write(doc)

report()