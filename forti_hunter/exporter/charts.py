import matplotlib.pyplot as plt
import pandas as pd
import os

def make_charts(stats, output_dir, output_files):
    print("======= 產生圖表（Charts） =======")

    # --- 來源國家排行（ISO2） ---
    df_country = stats.get("src_country_counts_df")
    if df_country is not None and not df_country.empty:

        # v6 欄位必定為 country_iso2 / count
        if "country_iso2" in df_country.columns:
            plt.figure(figsize=(10, 5))
            df_country.set_index("country_iso2")["count"].plot(
                kind="bar",
                color="steelblue"
            )
            plt.title("Top Source Countries (ISO2)")
            plt.xlabel("Country (ISO2)")
            plt.ylabel("Hit Count")
            plt.xticks(rotation=45)

            fname = os.path.join(output_dir, "src_country_stats.png")
            plt.tight_layout()
            plt.savefig(fname)
            plt.close()
            output_files.append(fname)
        else:
            print("⚠ src_country_counts_df 缺少欄位 country_iso2")

    # --- Top 10 來源 IP ---
    df_src_ip = stats.get("src_ip_counts_df")
    if df_src_ip is not None and not df_src_ip.empty:
        plt.figure(figsize=(10, 5))
        top10 = df_src_ip.head(10).set_index("srcip")["count"]
        top10.plot(kind="bar", color="darkorange")
        plt.title("Top 10 Source IP")
        plt.xlabel("Source IP")
        plt.ylabel("Hit Count")
        plt.xticks(rotation=45)

        fname = os.path.join(output_dir, "src_ip_top10.png")
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        output_files.append(fname)

    # --- 趨勢折線圖 ---
    df_trend = stats.get("trend_df")
    if df_trend is not None and not df_trend.empty:
        plt.figure(figsize=(10, 5))
        temp = df_trend.copy()
        temp["date"] = pd.to_datetime(temp["date"], errors="coerce")
        temp = temp.dropna(subset=["date"]).set_index("date").sort_index()

        temp["hits"].plot(kind="line", marker="o", color="green")
        plt.title("Daily Blacklist Hits")
        plt.xlabel("Date")
        plt.ylabel("Hits")
        plt.xticks(rotation=45)

        fname = os.path.join(output_dir, "blacklist_trend.png")
        plt.tight_layout()
        plt.savefig(fname)
        plt.close()
        output_files.append(fname)
