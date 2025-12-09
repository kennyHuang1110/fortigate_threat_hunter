import pandas as pd

def compute_stats(df):

    stats = {}

    # === 來源國家統計 ===
    if "srccountry" in df.columns:
        src_country_df = (
            df.groupby("srccountry")
              .size()
              .reset_index(name="count")
              .rename(columns={"srccountry": "country_iso2"})
        )
        stats["src_country_counts_df"] = src_country_df.sort_values("count", ascending=False)
    else:
        stats["src_country_counts_df"] = pd.DataFrame(columns=["country_iso2", "count"])

    # === 目的國家統計 ===
    if "dstcountry" in df.columns:
        dst_country_df = (
            df.groupby("dstcountry")
              .size()
              .reset_index(name="count")
              .rename(columns={"dstcountry": "country_iso2"})
        )
        stats["dst_country_counts_df"] = dst_country_df.sort_values("count", ascending=False)
    else:
        stats["dst_country_counts_df"] = pd.DataFrame(columns=["country_iso2", "count"])

    # === 來源 IP 統計 ===
    if "srcip" in df.columns:
        src_ip_df = df.groupby("srcip").size().reset_index(name="count")
        stats["src_ip_counts_df"] = src_ip_df.sort_values("count", ascending=False)
    else:
        stats["src_ip_counts_df"] = pd.DataFrame(columns=["srcip", "count"])

    # === 目的 IP 統計 ===
    if "dstip" in df.columns:
        dst_ip_df = df.groupby("dstip").size().reset_index(name="count")
        stats["dst_ip_counts_df"] = dst_ip_df.sort_values("count", ascending=False)
    else:
        stats["dst_ip_counts_df"] = pd.DataFrame(columns=["dstip", "count"])

    # === 與 service 統計 ===
    if "service" in df.columns:
        service_df = df.groupby("service").size().reset_index(name="count")
        stats["service_counts_df"] = service_df.sort_values("count", ascending=False)
    else:
        stats["service_counts_df"] = pd.DataFrame(columns=["service", "count"])

    # === 與 policyid 統計 ===
    if "policyid" in df.columns:
        pol_df = df.groupby("policyid").size().reset_index(name="count")
        stats["policy_counts_df"] = pol_df.sort_values("count", ascending=False)
    else:
        stats["policy_counts_df"] = pd.DataFrame(columns=["policyid", "count"])

    # === 趨勢統計（按日期） ===
    if "date" in df.columns:
        trend_df = df.groupby("date").size().reset_index(name="hits")
        stats["trend_df"] = trend_df.sort_values("date")
    else:
        stats["trend_df"] = pd.DataFrame(columns=["date", "hits"])

    return stats
