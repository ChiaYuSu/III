
<h1>{case}</h1>
- 查詢案例：{caseName}

---

<h2>特徵 1 – 熱度</h2>
<h3>圖形定義</h3>

- X 軸：案例傳播期間且以一個月作為間隔
- Y 軸：節點數量
- 規則：將有最多節點的月份設為基準月，基準月的節點數量乘上 25% 作為臨界線（紅線），當單月節點數量（基準月除外）的數值超過臨界線，列為高風險。若無任何單月節點數量（基準月除外）超過臨界線，則列為低風險

<h3>風險值定義</h3>

- 高風險：任一節點高於紅線（基準月除外）
- 低風險：所有節點皆低於紅線（基準月除外）

<h3>熱度圖</h3>
<div class="embed-responsive embed-responsive-16by9">
  <iframe
    class="embed-responsive-item"
    src="{feature1}"
    style="border: 0"
  ></iframe>
</div>

<h3>熱度分析</h3>
{quantity1}

<h3>特徵風險值</h3>
<div class="alert" role="alert" style="background-color: #{cfbg1}; color: #{cfft1}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf1_1} risk!</h4>
  <p>{cf1}</p>
  <hr style="border-color: #{cfhr1}">
  <p class="mb-0">特徵 1 – {rf1_2}風險</p>
</div>

---

<h2>特徵 2 – 時間跨度</h2>
<h3>圖形定義</h3>

- X 軸：案例傳播期間
- Y 軸：層數
- 規則：單一節點於 3 天之內未有任何上層連接節點，而 3 天之後卻出現上層連接節點。當案例中有一節點出現上述情形，則判斷為高風險

<h3>風險值定義</h3>

- 高風險：圖表中出現任一紅線與紅點
- 低風險：圖表中皆為藍線及藍點

<h3>傳播圖</h3>
<div class="embed-responsive embed-responsive-16by9">
  <iframe
    class="embed-responsive-item"
    src="{feature2}"
    style="border: 0"
  ></iframe>
</div>

<h3>時間跨度大</h3>
{feature2_2}

<h3>特徵風險值</h3>
<div class="alert" role="alert" style="background-color: #{cfbg2}; color: #{cfft2}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf2_1} risk!</h4>
  <p>{cf2}</p>
  <hr style="border-color: #{cfhr2}">
  <p class="mb-0">特徵 2 – {rf2_2}風險</p>
</div>

---

<h2>特徵 3 – 白名單與查核驗證</h2>
<h3>規則定義</h3>
<h4>安全因素</h4>

- 將各大主流媒體的 Facebook URL 及網頁 URL 紀錄於白名單中，若爬蟲的原始資料出現白名單的資訊，會依照出現的類型列進「安全因素」當中並計次數，以下為「安全因素」的三種類型：
    - Match URL
    - Match `related_link`
    - Match `author_id`

<h4>風險因素</h4>

- 以台灣事實查核中心（TFC）與 MyGoPen 兩大查核網站為識別依據，若單篇案例的爬蟲原始資料出現事實查核機構的資訊，或是出現多數民眾認為消息不實所發表的評論，則該案例有風險是虛假消息。依照出現的類型列進「風險因素」當中並計次數，以下為「風險因素」的三種類型：
    - Match URL
    - Match `body` of the article
    - Match `body` of the comment

<h3>風險值定義</h3>

- 「安全因素」與「風險因素」所得之分數進行相抵，可分為三種風險評測結果：
    - 高風險：安全因素 - 風險因素 < 0
    - 中風險：0 ≤ 安全因素 - 風險因素 < 4
    - 低風險：安全因素 - 風險因素 ≥ 4

<h3>安全因素</h3>
{feature3}

<h3>風險因素</h3>
{feature3_2}

<h3>特徵風險值</h3>
<div class="alert" role="alert" style="background-color: #{cfbg3}; color: #{cfft3}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf3_1} risk!</h4>
  <p>{cf3}</p>
  <hr style="border-color: #{cfhr3}">
  <p class="mb-0">特徵 3 – {rf3_2}風險</p>
</div>

---

<h2>特徵 4 – 意圖語意判別</h2>
<h3>風險值定義</h3>

- 在網路中的錯誤訊息除了標題會使用較聳動的字詞，還可能在文章一開始或結尾加上要求轉發及分享等語句。利用案例的爬蟲原始資料將內容出現類似要求轉發、轉傳或分享等意圖的語句加以計數，作為權衡可能為錯誤訊息的風險依據之一，以下為風險評估標準：
    - 高風險：意圖語句總數 ≥ 10
    - 中風險：3 ≤ 意圖語句總數 < 10
    - 低風險：意圖語句總數 < 3

<h3>分享內容包含高風險字詞</h3>
{feature4}

<h3>特徵風險值</h3>
<div class="alert" role="alert" style="background-color: #{cfbg4}; color: #{cfft4}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf4_1} risk!</h4>
  <p>{cf4}</p>
  <hr style="border-color: #{cfhr4}">
  <p class="mb-0">特徵 4 – {rf4_2}風險</p>
</div>

---

<h2>特徵 5 – 首次分享與留言的時間差</h2>
<h3>風險值定義</h3>

- 正常情況下的新聞會由主流媒體所發佈，傳播的初期就會有最大的聲量，進而可觀察到社群平台上發佈留言與分享的時間會較於集中。因此推論當案例為錯誤訊息時，首次留言與首次分享的時隔會較長，以下為此特徵之風險評估標準：
    - 高風險：時間差 > 60 分鐘
    - 中風險：30 分鐘 ≤ 時間差 ≤ 60 分鐘
    - 低風險：時間差 < 30 分鐘

<h3>時間差</h3>
{feature5}

<h3>特徵風險值</h3>
<div class="alert" role="alert" style="background-color: #{cfbg5}; color: #{cfft5}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf5_1} risk!</h4>
  <p>{cf5}</p>
  <hr style="border-color: #{cfhr5}">
  <p class="mb-0">特徵 5 – {rf5_2}風險</p>
</div>

---

<h2>特徵 6 – 貼文平均傳播時間</h2>
<h3>風險值定義</h3>

- 正常情況下的新聞由主流媒體所發佈，可發現討論度大多集中於傳播初期，貼文之間的時間間隔短且密集，因此推論錯誤訊息的貼文之間的時間間隔可能拉得較長且分散，以下為此特徵之風險評估標準：
    - 高風險：平均傳播時間 > 5 小時
    - 中風險：2 小時 ≤ 平均傳播時間 ≤ 5 小時
    - 低風險：平均傳播時間 < 2 小時 
- 公式定義：
    - 貼文平均傳播時間 = Σ 兩個貼文之間的時間差 ÷ 時間差個數




<h3>時間差</h3>
{feature6}

<h3>特徵風險值</h3>
<div class="alert" role="alert" style="background-color: #{cfbg6}; color: #{cfft6}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf6_1} risk!</h4>
  <p>{cf6}</p>
  <hr style="border-color: #{cfhr6}">
  <p class="mb-0">特徵 6 – {rf6_2}風險</p>
</div>

---

<h2>結論</h2>
所以根據以上特徵分析結果，{case2} 為{risk}風險。
