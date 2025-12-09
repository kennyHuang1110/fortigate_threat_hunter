import os
import pandas as pd

def export_excel(stats, matched, output_dir, output_files):

    out_path = os.path.join(output_dir, "fortigate_analysis.xlsx")

    with pd.ExcelWriter(out_path, engine="openpyxl") as writer:

        # === 全部惡意紀錄 ===
        matched.to_excel(writer, sheet_name="matched_logs", index=False)

        # === 來源國家 ===
        stats["src_country_counts_df"].to_excel(writer, sheet_name="src_country", index=False)

        # === 目的國家 ===
        stats["dst_country_counts_df"].to_excel(writer, sheet_name="dst_country", index=False)

        # === Top 來源 IP ===
        stats["src_ip_counts_df"].to_excel(writer, sheet_name="src_ip", index=False)

        # === Top 目的 IP ===
        stats["dst_ip_counts_df"].to_excel(writer, sheet_name="dst_ip", index=False)

        # === Top service ===
        stats["service_counts_df"].to_excel(writer, sheet_name="service", index=False)

        # === Top policy ===
        stats["policy_counts_df"].to_excel(writer, sheet_name="policy", index=False)

        # === 每日惡意趨勢 ===
        stats["trend_df"].to_excel(writer, sheet_name="trend", index=False)

    output_files.append(out_path)
    print(f"✔ 已輸出 Excel：{out_path}")
