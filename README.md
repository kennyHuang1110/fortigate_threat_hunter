# 🔍 Forti Hunter — Fortigate Log Threat Hunting 工具

Forti Hunter 是一套針對 Fortigate 防火牆輸出 Log 的**攻擊行為分析工具**，  
支援地理位置比對、黑名單偵測、Whois 查詢、統計圖表輸出等功能，  
並以純 Python 讓資安研究人員快速 Threat Hunting。

---

## 🚀 核心功能

- 📂 解析 Fortigate disk-traffic-forward log（大量日誌）
- 🧠 智慧分類掃描、連線異常
- 🌍 GeoIP 定位來源國家
- 📊 產生攻擊來源統計圖表
- 📝 Excel 分析報表輸出
- 🔎 Whois / ASN 查詢
- ⚡ 自動產生 `.env` 組態檔
- 🧭 跨平台支援（Windows / Linux）

---

## 📦 專案結構

forti_hunter/
│
├── analyzer/ ← Log 解析核心
├── core/ ← 公用函式
├── exporter/ ← Excel / 圖表輸出
├── geo/ ← GeoIP 功能
├── whois_mod/ ← Whois / ASN
├── main.py ← 主程式入口
├── .env ← 組態 (不會上 repo)
└── requirements.txt ← 套件需求


---

## 🛠️ 安裝方式（Windows）

```bash
python --version

python -m venv venv
venv\Scripts\activate

pip install -r requirements.txt

