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
quantity1 = quantity1.append(f1_2, ignore_index=True).set_index("Month")
quantity1 = quantity1.to_markdown()

feature2 = plot.case + "\\feature2.html"

f3 = {'Match URL (Google search crawler)': plot.tmp, 'Match `related_link` (JSON)': plot.tmp3,
      'Match `author_id` (JSON)': plot.tmp4+plot.tmp5}
quantity3 = pd.Series(f3)
quantity3 = quantity3.rename("Quantity")
feature3 = quantity3.to_markdown()
f3_2 = {'Exclude fake, rumor and other related words (Google search crawler)': plot.tmp2, 'Match URL (Google search crawler)': plot.tmp6}
quantity3_2 = pd.Series(f3_2)
quantity3_2 = quantity3_2.rename("Quantity")
feature3_2 = quantity3_2.to_markdown()

f4 = {'Content': plot.fakeWords, "Quantity": plot.fakeWordsCount}
feature4 = pd.DataFrame(f4)
feature4 = feature4[~(feature4 == 0).any(axis=1)]
feature4 = feature4.sort_values(by=['Quantity'], ascending=False)
f4_2 = {'Content': 'Total', 'Quantity': sum(plot.fakeWordsCount)}
feature4 = feature4.append(f4_2, ignore_index=True).set_index("Content")
feature4 = feature4.to_markdown()

f5 = {'Type': ['First share time', 'First comment time', 'Time gap'], 'Time': plot.commentShareTime}
feature5 = pd.DataFrame(f5).set_index("Type")
feature5 = feature5.to_markdown()

f6 = {'Date': plot.postTime, 'Time Gap': plot.timeListGap}
feature6 = pd.DataFrame(f6)
f6_2 = {'Date': 'Average', 'Time Gap': plot.average}
feature6 = feature6.append(f6_2, ignore_index=True)
feature6 = feature6[~(feature6 == 0).any(axis=1)].set_index("Date")
feature6 = feature6.to_markdown()


md_template = open(r'markdown_template.md', encoding='utf8').read()
md = md_template.format(case=case, caseName=caseName, feature1=feature1, quantity1=quantity1,
                        feature2=feature2, feature3=feature3, feature3_2=feature3_2, feature4=feature4, feature5=feature5, feature6 = feature6)
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
