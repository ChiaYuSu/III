---

# {case}
- 查詢案例：{caseName}

---

## 特徵 1 -- 熱度
### 圖形定義
- X 軸：案例傳播期間且以一個月作為間隔
- Y 軸：節點數量
- 規則：將有最多節點的月份設為基準月，基準月的節點數量乘上 25% 作為臨界線（紅線），當單月節點數量（基準月除外）的數值超過臨界線，列為高風險。若無任何單月節點數量（基準月除外）超過臨界線，則列為低風險

### 風險值定義
- 高風險：任一節點高於紅線（基準月除外）
- 低風險：所有節點皆低於紅線（基準月除外）

### 熱度圖
<div class="embed-responsive embed-responsive-16by9">
  <iframe
    class="embed-responsive-item"
    src="{feature1}"
    style="border: 0"
  ></iframe>
</div>

### 熱度分析
{quantity1}

### 結論
<div class="alert" role="alert" style="background-color: #{cfbg1}; color: #{cfft1}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf1_1} risk!</h4>
  <p>{cf1}</p>
  <hr style="border-color: #{cfhr1}">
  <p class="mb-0">特徵 1 -- {rf1_2}風險</p>
</div>

---

## 特徵 2 -- 時間跨度
### 圖形定義
- X 軸：案例傳播期間
- Y 軸：層數
- 規則：單一節點於 3 天之內未有任何上層連接節點，而 3 天之後卻出現上層連接節點。當案例中有一節點出現上述情形，則判斷為高風險

### 風險值定義
- 高風險：圖表中出現任一紅線與紅點
- 低風險：圖表中皆為藍線及藍點

### 傳播圖
<div class="embed-responsive embed-responsive-16by9">
  <iframe
    class="embed-responsive-item"
    src="{feature2}"
    style="border: 0"
  ></iframe>
</div>

### 時間跨度大
{feature2_2}

### 結論
<div class="alert" role="alert" style="background-color: #{cfbg2}; color: #{cfft2}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf2_1} risk!</h4>
  <p>{cf2}</p>
  <hr style="border-color: #{cfhr2}">
  <p class="mb-0">特徵 2 -- {rf2_2}風險</p>
</div>

---

## 特徵 3 -- 白名單與查核驗證
### 規則定義
#### 安全因素
- 將各大主流媒體的 Facebook URL 及網頁 URL 紀錄於白名單中，若爬蟲的原始資料出現白名單的資訊，會依照出現的類型列進「安全因素」當中並計次數，以下為「安全因素」的三種類型：
    - Match URL
    - Match `related_link`
    - Match `author_id`

#### 風險因素
- 以台灣事實查核中心（TFC）與 MyGoPen 兩大查核網站為識別依據，若單篇案例的爬蟲原始資料出現事實查核機構的資訊，或是出現多數民眾認為消息不實所發表的評論，則該案例有風險是虛假消息。依照出現的類型列進「風險因素」當中並計次數，以下為「風險因素」的三種類型：
    - Match URL
    - Match `body` of the article
    - Match `body` of the comment

### 風險值定義
- 「安全因素」與「風險因素」所得之分數進行相抵，可分為三種風險評測結果：
    - 高風險：安全因素 - 風險因素 < 0
    - 中風險：0 ≤ 安全因素 - 風險因素 < 4
    - 低風險：安全因素 - 風險因素 ≥ 4

### 安全因素
{feature3}

### 風險因素
{feature3_2}

### 結論
<div class="alert" role="alert" style="background-color: #{cfbg3}; color: #{cfft3}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf3_1} risk!</h4>
  <p>{cf3}</p>
  <hr style="border-color: #{cfhr3}">
  <p class="mb-0">特徵 3 -- {rf3_2}風險</p>
</div>

---

## 特徵 4 -- 語意
### 風險值定義

### 分享內容包含高風險字詞
{feature4}

### 結論
<div class="alert" role="alert" style="background-color: #{cfbg4}; color: #{cfft4}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf4_1} risk!</h4>
  <p>{cf4}</p>
  <hr style="border-color: #{cfhr4}">
  <p class="mb-0">特徵 4 -- {rf4_2}風險</p>
</div>

---

## 特徵 5 -- 第一則留言與第一則分享時間差
### 風險值定義

### 時間差
{feature5}

### 結論
<div class="alert" role="alert" style="background-color: #{cfbg5}; color: #{cfft5}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf5_1} risk!</h4>
  <p>{cf5}</p>
  <hr style="border-color: #{cfhr5}">
  <p class="mb-0">特徵 5 -- {rf5_2}風險</p>
</div>

---

## 特徵 6 -- 貼文與貼文時間差
### 風險值定義

### 時間差
{feature6}

### 結論
<div class="alert" role="alert" style="background-color: #{cfbg6}; color: #{cfft6}">
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf6_1} risk!</h4>
  <p>{cf6}</p>
  <hr style="border-color: #{cfhr6}">
  <p class="mb-0">特徵 6 -- {rf6_2}風險</p>
</div>

---

## 結果
所以根據以上特徵分析結果，{case2} 為{risk}風險。

---
<div style="color: #ABABAB; text-align: center; margin-bottom: 40px">Copyright © 2020 財團法人資訊工業策進會 版權所有</div>