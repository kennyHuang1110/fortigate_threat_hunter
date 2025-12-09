import pandas as pd
from forti_thunter.core.config import MAX_WHOIS_SRC_IP, MAX_WHOIS_DST_IP

# 可選：如果沒裝這些套件，只會略過，不會炸掉
try:
    from ipwhois import IPWhois
    _IPWHOIS_OK = True
except Exception:
    _IPWHOIS_OK = False

try:
    import whois
    _WHOIS_OK = True
except Exception:
    _WHOIS_OK = False


_asn_cache = {}
_whois_cache = {}


def lookup_asn(ip: str):
    if not _IPWHOIS_OK:
        return None, None
    if ip in _asn_cache:
        return _asn_cache[ip]
    try:
        obj = IPWhois(ip)
        res = obj.lookup_rdap(asn_methods=["whois", "http"])
        asn = res.get("asn")
        asn_desc = res.get("asn_description")
        _asn_cache[ip] = (asn, asn_desc)
        return asn, asn_desc
    except Exception:
        _asn_cache[ip] = (None, None)
        return None, None


def lookup_whois_org(ip: str):
    """簡單 whois，取得 org/registrant/名稱資訊"""
    if not _WHOIS_OK:
        return None
    if ip in _whois_cache:
        return _whois_cache[ip]
    try:
        res = whois.whois(ip)
        org = res.get("org") or res.get("name") or res.get("registrar")
        _whois_cache[ip] = org
        return org
    except Exception:
        _whois_cache[ip] = None
        return None


def enrich_whois_asn(df: pd.DataFrame) -> pd.DataFrame:
    """只對 Top N src/dst IP 做 ASN / Whois enrich，避免過慢"""

    df = df.copy()

    # Top src / dst IP
    top_src_ips = df["srcip"].value_counts().head(MAX_WHOIS_SRC_IP).index.tolist()
    top_dst_ips = df["dstip"].value_counts().head(MAX_WHOIS_DST_IP).index.tolist()

    src_asn_map = {}
    src_org_map = {}
    dst_asn_map = {}
    dst_org_map = {}

    # 來源 IP enrich
    for ip in top_src_ips:
        asn, asname = lookup_asn(ip)
        org = lookup_whois_org(ip)
        src_asn_map[ip] = (asn, asname)
        src_org_map[ip] = org

    # 目的 IP enrich
    for ip in top_dst_ips:
        asn, asname = lookup_asn(ip)
        org = lookup_whois_org(ip)
        dst_asn_map[ip] = (asn, asname)
        dst_org_map[ip] = org

    def _get_src_asn(ip):
        return src_asn_map.get(ip, (None, None))[0]

    def _get_src_asname(ip):
        return src_asn_map.get(ip, (None, None))[1]

    def _get_src_org(ip):
        return src_org_map.get(ip)

    def _get_dst_asn(ip):
        return dst_asn_map.get(ip, (None, None))[0]

    def _get_dst_asname(ip):
        return dst_asn_map.get(ip, (None, None))[1]

    def _get_dst_org(ip):
        return dst_org_map.get(ip)

    df["src_asn"] = df["srcip"].map(_get_src_asn)
    df["src_asname"] = df["srcip"].map(_get_src_asname)
    df["src_whois_org"] = df["srcip"].map(_get_src_org)

    df["dst_asn"] = df["dstip"].map(_get_dst_asn)
    df["dst_asname"] = df["dstip"].map(_get_dst_asname)
    df["dst_whois_org"] = df["dstip"].map(_get_dst_org)

    return df
