# 電商特價優惠爬蟲

## 簡介

這是一個用 python requests 抓取商品優惠的爬蟲\
目前實作了抓取臺灣 Costco 的優惠資訊並且存入 SQLite\
使用了模組化的開發 將 DB 的 ORM 獨立出來方便抽換底層及前後處理\
在 `crawler/__init__.py` 中則是使用了 Singleton 的方法避免重複建立 DB instance\
在 `crawler/__main__.py` 中將流程串接起來:
1. 抓取網頁 api (或使用 local 檔案)
2. 從 Singleton 中取得 DB instance
3. 將資料 parse 後實例化為 CostoProduct 物件
4. 將物件存入 DB
5. 將 DB 中所有物件讀出
6. 存入 txt 檔案

## 定時執行

目前使用簡單的 time 來計時執行\
比較好的做法應該是在 host 上使用 cronjob 或其他排程工具來執行\
這樣可以避免在本機掛著程式

## OO 設計

在 `crawler/lib` 中有兩個 product 的 class\
`Product` 是一個抽象類別\
`CostcoProduct` 繼承自 `Product`\
這樣可以讓程式更有彈性\
若未來要新增其他電商的爬蟲\
只需要新增一個新的 class 繼承自 `Product`\
並且實作實例化方法即可

在 `crawler/db/costco.py` 中使用了 class decorator 來實作 error handler 及 connection handler \
這樣可以讓程式更為乾淨\
不需要在每個 method 中都寫上 try except\
也不需要在每個 method 中都寫上 connection 的建立及關閉


## 使用方法

### Pipenv

```bash
pipenv install
pipenv run crawler
```

### Pip

```bash
pip install -r requirements.txt
python -m crawler
```
