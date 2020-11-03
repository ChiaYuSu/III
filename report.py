import os
import codecs as co
import markdown
import plot
import pandas as pd
from pathlib import Path
from datetime import datetime

# Case
case = plot.case
caseName = plot.query

feature1 = plot.case + "\\feature1.html"
dateTime = []
for i in plot.dateTimeMonth:
    dateTime.append(i[0:10])
f1 = {'Month': dateTime, 'Quantity': plot.amount}
quantity1 = pd.DataFrame(f1)
quantity1 = quantity1[~(quantity1 == 0).any(axis=1)]
quantity1 = quantity1.sort_values(by=['Quantity'], ascending=False)
f1_2 = {'Month': 'Total', 'Quantity': sum(plot.amount)}
quantity1 = quantity1.append(f1_2, ignore_index=True).set_index('Month')
quantity1 = quantity1.to_markdown()

count = 0
if plot.quarterLine > 0:
    cfbg1 = "F8D7DA"
    cfft1 = "721C24"
    cfhr1 = "F1B0B7"
    rf1_1 = "High"
    rf1_2 = "高"
    time = ""
    count = 0
    for i in plot.timeCount25:
        if len(plot.timeCount25) == 1:
            time += i
        else:
            if count == len(plot.timeCount25)-1:
                time = time[:-1]
                time +=  " 與 " + i
            elif count != len(plot.timeCount25)-1:
                time += i + "、"
                count += 1
    cf1 = plot.case + " 在 " + time + " 高於 Critical line，所以針對此輸出結果，將特徵 1 判斷為高風險。"
elif plot.quarterLine == 0:
    cfbg1 = "D4EDDA"
    cfft1 = "155724"
    cfhr1 = "B1DFBB"
    rf1_1 = "Low"
    rf1_2 = "低"
    cf1 = plot.case + " 皆沒有任何一點高於 Critical line，所以針對此輸出結果，將特徵 1 判斷為低風險。"

feature2 = plot.case + "\\feature2.html"
f2_2= {"Original date": plot.parentTime2, 'Later date': plot.articleTime2, 'Time gap': plot.timeGap2}
feature2_2 = pd.DataFrame(f2_2)
feature2_2 = feature2_2.set_index('Original date').sort_values(by=['Original date'])
feature2_2 = feature2_2.to_markdown()

if plot.feature2 > 0:
    cfbg2 = "F8D7DA"
    cfft2 = "721C24"
    cfhr2 = "F1B0B7"
    rf2_1 = "High"
    rf2_2 = "高"
    cf2 = plot.case + " 在上述列表中曾出現過時間跨度大的現象，所以針對此輸出結果，將特徵 2 判斷為高風險。"
elif plot.feature2 == 0:
    cfbg2 = "D4EDDA"
    cfft2 = "155724"
    cfhr2 = "B1DFBB"
    rf2_1 = "Low"
    rf2_2 = "低"
    cf2 = plot.case + " 在上述列表中未曾出現過時間跨度大的現象，所以針對此輸出結果，將特徵 2 判斷為低風險。"

f3 = {'Match URL': plot.tmp, 'Match `related_link`': plot.tmp3,
    'Match `author_id`': plot.tmp4+plot.tmp5}
quantity3 = pd.Series(f3)
quantity3 = quantity3.rename('Quantity')
feature3 = quantity3.to_markdown()
f3_2 = {'Match URL': plot.tmp2,
        'Match `body` of the article': plot.tmp6,
        'Match `body` of the comment': plot.tmp7}
quantity3_2 = pd.Series(f3_2)
quantity3_2 = quantity3_2.rename('Quantity')
feature3_2 = quantity3_2.to_markdown()

white = plot.tmp + plot.tmp3 + plot.tmp4 + plot.tmp5
black = plot.tmp2 + plot.tmp6 + plot.tmp7
if plot.feature3 < 0:
    cfbg3 = "F8D7DA"
    cfft3 = "721C24"
    cfhr3 = "F1B0B7"
    rf3_1 = "High"
    rf3_2 = "高"
    cf3 = plot.case + " 由於安全因素 (" + str(white) + ") - 風險因素 (" + str(black) + ") < 0，所以針對此輸出結果，將特徵 3 判斷為高風險。"
elif plot.feature3 >= 0 and plot.feature3 < 4:
    cfbg3 = "FFF3CD"
    cfft3 = "856404"
    cfhr3 = "FFE8A1"
    rf3_1 = "Median"
    rf3_2 = "中"
    cf3 = plot.case + " 由於安全因素 (" + str(white) + ") - 風險因素 (" + str(black) + ") 介於 0 到 4 之間，所以針對此輸出結果，將特徵 3 判斷為中風險。"
elif plot.feature3 >= 4:
    cfbg3 = "D4EDDA"
    cfft3 = "155724"
    cfhr3 = "B1DFBB"
    rf3_1 = "Low"
    rf3_2 = "低"
    cf3 = plot.case + " 由於安全因素 (" + str(white) + ") - 風險因素 (" + str(black) + ") ≥ 4，所以針對此輸出結果，將特徵 3 判斷為低風險。"

f4 = {'Content': plot.fakeWords2, 'Quantity': plot.fakeWordsCount2}
feature4 = pd.DataFrame(f4)
feature4 = feature4[~(feature4 == 0).any(axis=1)]
feature4 = feature4.sort_values(by=['Quantity'], ascending=False)
f4_2 = {'Content': 'Total', 'Quantity': sum(plot.fakeWordsCount2)}
feature4 = feature4.append(f4_2, ignore_index=True).set_index('Content')
feature4 = feature4.to_markdown()

if plot.feature4 >= 10:
    cfbg4 = "F8D7DA"
    cfft4 = "721C24"
    cfhr4 = "F1B0B7"
    rf4_1 = "High"
    rf4_2 = "高"
    cf4 = plot.case + " 在分享內文中出現過 ≥ 10 次的高風險字詞，所以針對此輸出結果，將特徵 4 判斷為高風險。"
elif plot.feature4 >= 3 and plot.feature4 < 10:
    cfbg4 = "FFF3CD"
    cfft4 = "856404"
    cfhr4 = "FFE8A1"
    rf4_1 = "Median"
    rf4_2 = "中"
    cf4 = plot.case + " 在分享內文中出現過介於 3 到 10 次的高風險字詞，所以針對此輸出結果，將特徵 4 判斷為中風險。"
elif plot.feature4 >= 0 and plot.feature4 < 3:
    cfbg4 = "D4EDDA"
    cfft4 = "155724"
    cfhr4 = "B1DFBB"
    rf4_1 = "Low"
    rf4_2 = "低"
    cf4 = plot.case + " 在分享內文中出現過介於 0 到 3 次的高風險字詞，所以針對此輸出結果，將特徵 4 判斷為低風險。"

f5 = {'Type': ['First share time', 'First comment time',
            'Time gap'], 'Time': plot.commentShareTime}
feature5 = pd.DataFrame(f5).set_index('Type')
feature5 = feature5.to_markdown()

if plot.feature5 > 3600:
    cfbg5 = "F8D7DA"
    cfft5 = "721C24"
    cfhr5 = "F1B0B7"
    rf5_1 = "High"
    rf5_2 = "高"
    cf5 = plot.case + " 第一則留言與第一則分享時間差 > 60 分鐘，所以針對此輸出結果，將特徵 5 判斷為高風險。"
elif plot.feature5 > 1800 and plot.feature5 <= 3600:
    cfbg5 = "FFF3CD"
    cfft5 = "856404"
    cfhr5 = "FFE8A1"
    rf5_1 = "Median"
    rf5_2 = "中"
    cf5 = plot.case + " 第一則留言與第一則分享時間差介於 30 分鐘至 60 分鐘，所以針對此輸出結果，將特徵 5 判斷為中風險。"
elif plot.feature5 <= 1800:
    cfbg5 = "D4EDDA"
    cfft5 = "155724"
    cfhr5 = "B1DFBB"
    rf5_1 = "Low"
    rf5_2 = "低"
    cf5 = plot.case + " 第一則留言與第一則分享時間差 ≤ 30 分鐘，所以針對此輸出結果，將特徵 5 判斷為低風險。"

f6 = {'Date': plot.postTime, 'Time Gap': plot.timeListGap}
feature6 = pd.DataFrame(f6)
f6_2 = {'Date': 'Average', 'Time Gap': plot.average}
feature6 = feature6.append(f6_2, ignore_index=True)
feature6 = feature6[~(feature6 == 0).any(axis=1)].set_index('Date')
feature6 = feature6.to_markdown()

if plot.feature6 > 18000:
    cfbg6 = "F8D7DA"
    cfft6 = "721C24"
    cfhr6 = "F1B0B7"
    rf6_1 = "High"
    rf6_2 = "高"
    cf6 = plot.case + " 兩貼文之間時間差 > 5 小時，所以針對此輸出結果，將特徵 6 判斷為高風險。"
elif plot.feature6 >= 7200 and plot.feature6 <= 18000:
    cfbg6 = "FFF3CD"
    cfft6 = "856404"
    cfhr6 = "FFE8A1"
    rf6_1 = "Median"
    rf6_2 = "中"
    cf6 = plot.case + " 兩貼文之間時間差介於 2 小時到 5 小時之間，所以針對此輸出結果，將特徵 6 判斷為中風險。"
elif plot.feature6 < 7200:
    cfbg6 = "D4EDDA"
    cfft6 = "155724"
    cfhr6 = "B1DFBB"
    rf6_1 = "Low"
    rf6_2 = "低"
    cf6 = plot.case + " 兩貼文之間時間差 < 2 小時，所以針對此輸出結果，將特徵 6 判斷為低風險。"
    
f7 = {'Type': ['First share time', 'The most popular node time',
            'Time gap'], 'Time': plot.f7time}
feature7 = pd.DataFrame(f7).set_index('Type')
feature7 = feature7.to_markdown()

if plot.feature7 >= 108000:
    cfbg7 = "F8D7DA"
    cfft7 = "721C24"
    cfhr7 = "F1B0B7"
    rf7_1 = "High"
    rf7_2 = "高"
    cf7 = plot.case + " 兩貼文之間時間差 > 30 小時，所以針對此輸出結果，將特徵 7 判斷為高風險。"
elif plot.feature7 == 0:
    cfbg7 = "FFF3CD"
    cfft7 = "856404"
    cfhr7 = "FFE8A1"
    rf7_1 = "Median"
    rf7_2 = "中"
    cf7 = plot.case + " 兩貼文之間時間差為 0，所以針對此輸出結果，將特徵 7 判斷為中風險。"
elif plot.feature7 < 108000:
    cfbg7 = "D4EDDA"
    cfft7 = "155724"
    cfhr7 = "B1DFBB"
    rf7_1 = "Low"
    rf7_2 = "低"
    cf7 = plot.case + " 兩貼文之間時間差 < 30 小時，所以針對此輸出結果，將特徵 7 判斷為低風險。"
    
case2 = plot.case
risk = "{低/中/高}"

md_template = open(r'markdown_template.md', encoding='utf8').read()
md = md_template.format(case=case, caseName=caseName, feature1=feature1, quantity1=quantity1,
                        cfbg1=cfbg1, cfft1=cfft1, rf1_1=rf1_1, cf1=cf1, cfhr1=cfhr1, rf1_2=rf1_2,
                        feature2=feature2, feature2_2=feature2_2, 
                        cfbg2=cfbg2, cfft2=cfft2, rf2_1=rf2_1, cf2=cf2, cfhr2=cfhr2, rf2_2=rf2_2,
                        feature3=feature3, feature3_2=feature3_2,
                        cfbg3=cfbg3, cfft3=cfft3, rf3_1=rf3_1, cf3=cf3, cfhr3=cfhr3, rf3_2=rf3_2,
                        feature4=feature4, 
                        cfbg4=cfbg4, cfft4=cfft4, rf4_1=rf4_1, cf4=cf4, cfhr4=cfhr4, rf4_2=rf4_2,
                        feature5=feature5, 
                        cfbg5=cfbg5, cfft5=cfft5, rf5_1=rf5_1, cf5=cf5, cfhr5=cfhr5, rf5_2=rf5_2,
                        feature6=feature6,
                        cfbg6=cfbg6, cfft6=cfft6, rf6_1=rf6_1, cf6=cf6, cfhr6=cfhr6, rf6_2=rf6_2,
                        feature7=feature7,
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
report = plot.case + ".html"
with open(report, 'w', encoding='utf-8') as f:
    f.write(doc)
    