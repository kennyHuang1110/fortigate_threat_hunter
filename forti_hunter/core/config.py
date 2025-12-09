import os
from dotenv import load_dotenv

load_dotenv()
# Log / Blacklist / GeoIP DB 檔案名稱
LOG_FILE = os.getenv("LOG_FILE")

BLACKLIST_FILE = "black_ips.txt"
GEOIP_DB = "GeoLite2-Country.mmdb"

# 預設輸出根目錄（可以改成你想要的 Base path）
OUTPUT_BASE_DIR = "."

# Whois/ASN 設定：為了避免太慢，只查前 N 個熱門 IP
MAX_WHOIS_SRC_IP = 200
MAX_WHOIS_DST_IP = 200
