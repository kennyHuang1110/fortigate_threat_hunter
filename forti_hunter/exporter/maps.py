import os
import pandas as pd
import plotly.express as px

# ======== 國家名稱 → ISO3（含中文 / 英文 / 別名） ========
ISO_NAME_MAP = {
    "United States": "USA", "USA": "USA", "US": "USA",
    "Germany": "DEU", "DE": "DEU",
    "Netherlands": "NLD", "NL": "NLD",
    "Thailand": "THA",
    "United Kingdom": "GBR", "UK": "GBR",
    "Malaysia": "MYS",
    "Brazil": "BRA",
    "Hong Kong": "HKG",
    "France": "FRA",
    "Nigeria": "NGA",
    "Japan": "JPN",
    "China": "CHN",
    "Taiwan": "TWN",
    "Singapore": "SGP",
    "Vietnam": "VNM",
    "South Korea": "KOR", "Korea": "KOR",
    "Russia": "RUS", "Russian Federation": "RUS",

    # 中文別名
    "美國": "USA", "德國": "DEU", "荷蘭": "NLD",
    "泰國": "THA", "英國": "GBR", "馬來西亞": "MYS",
    "巴西": "BRA", "香港": "HKG", "法國": "FRA",
    "尼日利亞": "NGA", "日本": "JPN", "中國": "CHN",
    "台灣": "TWN", "新加坡": "SGP", "越南": "VNM",
    "韓國": "KOR",
}

# ======== 名稱 / ISO2 / ISO3 → ISO3 統一轉換 ========
def to_iso3(value: str):
    if pd.isna(value):
        return None

    value = str(value).strip()

    # 1) 完全匹配（英文 / 中文）
    if value in ISO_NAME_MAP:
        return ISO_NAME_MAP[value]

    # 2) ISO2 → ISO3
    if len(value) == 2:
        try:
            import pycountry
            c = pycountry.countries.get(alpha_2=value.upper())
            if c:
                return c.alpha_3
        except:
            pass

    # 3) ISO3 → ISO3
    if len(value) == 3:
        return value.upper()

    return None


# ======== 地圖引擎 v8.2 ========
def make_maps(stats: dict, output_dir: str, output_files: list):
    print("======= 產生世界地圖 v8.2（Full Auto Mapping） =======")

    df = None
    for key in ["asn_country_df", "src_country_counts_df", "dst_country_counts_df"]:
        if key in stats and not stats[key].empty:
            df = stats[key].copy()
            print(f"✔ 使用：{key} 作為地圖資料來源")
            break

    if df is None:
        print("(略過地圖：無有效統計資料)")
        return

    # ======== 自動偵測國家欄位 ========
    candidate_cols = ["country", "srccountry", "dstcountry", "country_name", "country_iso2"]
    country_col = None

    for col in candidate_cols:
        if col in df.columns:
            country_col = col
            break

    if country_col is None:
        print("(略過地圖：找不到有用的國家欄位)")
        print("現有欄位：", df.columns.tolist())
        return

    print(f"✔ 偵測到國家欄位：{country_col}")

    # ======== ISO3 轉換 ========
    df["iso_a3"] = df[country_col].apply(to_iso3)
    df = df.dropna(subset=["iso_a3"])

    if df.empty:
        print("(略過地圖：所有國家無法映射到 ISO3)")
        return

    # ======== 產生地圖 ========
    try:
        fig = px.choropleth(
            df,
            locations="iso_a3",
            color="count",
            hover_name=country_col,
            color_continuous_scale="Viridis",
            title="Source Country Heatmap (v8.2 – Auto Mapping)"
        )
        out = os.path.join(output_dir, "country_heatmap_v8.html")
        fig.write_html(out)
        output_files.append(out)
        print(f"✔ 已輸出地圖：{out}")

    except Exception as e:
        print(f"(Plotly 地圖失敗：{e})")
