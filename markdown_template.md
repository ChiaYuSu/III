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
  <h4 class="alert-heading" style="font-size: 18pt; font-weight: bold">{rf1} risk!</h4>
  <p>{cf1}</p>
  <hr style="border-color: #{cfhr1}">
  <p class="mb-0">特徵 1 -- {rf2}風險</p>
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

---

## 特徵 3 -- 主流媒體
### 風險值定義
### 低風險因素
{feature3}

### 高風險因素
{feature3_2}

### 結論

---

## 特徵 4 -- 語意
### 風險值定義

### 分享內容包含高風險字詞
{feature4}

### 結論

---

## 特徵 5 -- 第一則留言與第一則分享時間差
### 風險值定義

### 時間差
{feature5}

### 結論

---

## 特徵 6 -- 貼文與貼文時間差
### 風險值定義

### 時間差
{feature6}

### 結論

---

## 結果
所以根據以上特徵分析結果，Case 304 為高風險。

---
<div style="color: #ABABAB; text-align: center; margin-bottom: 40px">Copyright © 2020 財團法人資訊工業策進會 版權所有</div>