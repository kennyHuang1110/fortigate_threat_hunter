from forti_hunter.core.config import LOG_FILE, BLACKLIST_FILE, OUTPUT_BASE_DIR
from forti_hunter.core.log_parser import parse_fortigate_rawlog, load_blacklist
from forti_hunter.geo.geoip_utils import enrich_geoip
from forti_hunter.whois_mod.whois_asn import enrich_whois_asn
from forti_hunter.analyzer.stats import compute_stats
from forti_hunter.analyzer.classify import add_attack_classification
from forti_hunter.exporter.charts import make_charts
from forti_hunter.exporter.maps import make_maps
from forti_hunter.exporter.excel_exporter import export_excel
from forti_hunter.exporter.summary import export_summary

import os


def main():
    print("\n=== FortiGate Threat Hunter v5 啟動 ===\n")

    out_dir_name = input("請輸入輸出資料夾名稱：").strip()
    if not out_dir_name:
        out_dir_name = "output"

    output_dir = os.path.join(OUTPUT_BASE_DIR, out_dir_name)
    os.makedirs(output_dir, exist_ok=True)

    # 1. 解析 FortiGate log
    print(f"\n[1] 解析 Log 檔案：{LOG_FILE}")
    all_df = parse_fortigate_rawlog(LOG_FILE)
    print(f"   ➜ 共解析 {len(all_df):,} 筆紀錄")

    # 2. 載入黑名單
    print(f"\n[2] 載入惡意 IP 清單：{BLACKLIST_FILE}")
    blacklist_ips = load_blacklist(BLACKLIST_FILE)
    print(f"   ➜ 黑名單 IP 共 {len(blacklist_ips):,} 個")

    # 3. 比對 srcip/dstip
    print("\n[3] 比對 srcip/dstip 是否命中黑名單...")
    matched = all_df[all_df["srcip"].isin(blacklist_ips) | all_df["dstip"].isin(blacklist_ips)].copy()
    print(f"   ➜ 偵測到惡意連線：{len(matched):,} 筆")

    # 4. GeoIP enrich
    print("\n[4] GeoIP 解析來源/目的國家 (GeoLite2-Country.mmdb)...")
    matched = enrich_geoip(matched)

    # # 5. Whois/ASN enrich（只針對熱門 IP 做，避免太慢）
    # print("\n[5] Whois / ASN 解析 (來源/目的 IP)...")
    # matched = enrich_whois_asn(matched)

    # 6. 生成統計資訊
    print("\n[6] 計算統計資訊 / TOP 排名 / 攻擊分類...")
    matched = add_attack_classification(matched)
    stats = compute_stats(matched)

    # 7. 匯出 Excel / CSV / Summary / 圖表 / 地圖
    output_files = []

    # CSV & Excel
    export_excel(stats, matched, output_dir, output_files)

    # 圖表
    make_charts(stats, output_dir, output_files)

    # 地圖（Plotly）
    make_maps(stats, output_dir, output_files)

    # summary.txt
    export_summary(stats, all_df, matched, output_dir, output_files)

    print("\n=== 完成！所有輸出檔案如下 ===")
    for f in output_files:
        print(" -", f)


if __name__ == "__main__":
    main()

