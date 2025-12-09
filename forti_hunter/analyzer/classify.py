import pandas as pd


def classify_attack(row) -> tuple[str, str]:
    """
    根據 port / service / 協定做簡單分類
    回傳 (attack_type, attack_risk)
    """
    try:
        sport = int(row.get("srcport", 0))
        dport = int(row.get("dstport", 0))
    except Exception:
        sport = 0
        dport = 0

    svc = (row.get("service") or "").upper()
    proto = str(row.get("proto") or "")

    # 一些簡單的規則
    port = dport or sport

    # 高風險常見 port
    if port in (22, 2222):
        return "SSH 掃描/暴力破解", "高"
    if port == 23:
        return "Telnet 掃描/暴力破解", "高"
    if port in (3389, 3390):
        return "RDP 掃描/暴力破解", "高"
    if port in (1433, 3306, 1521):
        return "DB 掃描/暴力破解", "高"
    if port in (445, 139):
        return "SMB 掃描/橫向移動探測", "高"

    # Web 類別
    if port in (80, 8080, 8081) or "HTTP" in svc:
        return "Web 掃描/探測", "中"
    if port in (443, 8443) or "HTTPS" in svc:
        return "HTTPS 掃描/探測", "中"

    # DNS 類型
    if port == 53 or "DNS" in svc:
        return "DNS 查詢/異常流量", "低"

    # 其他
    if proto == "17":  # UDP
        return "一般 UDP 流量（可能掃描/探測）", "中"

    if proto == "6":  # TCP
        return "一般 TCP 流量（可能掃描/探測）", "中"

    return "未知/其他", "低"


def add_attack_classification(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    types = []
    risks = []
    for _, row in df.iterrows():
        t, r = classify_attack(row)
        types.append(t)
        risks.append(r)
    df["attack_type"] = types
    df["attack_risk"] = risks
    return df
