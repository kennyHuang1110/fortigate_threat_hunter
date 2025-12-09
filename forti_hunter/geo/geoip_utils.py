import pandas as pd
import geoip2.database
from forti_thunter.core.config import GEOIP_DB

_reader = geoip2.database.Reader(GEOIP_DB)


def ip_to_country(ip: str):
    """GeoLite2 查 IP → (國家名, ISO2, ISO3)，查不到回 Unknown"""
    try:
        resp = _reader.country(ip)
        name = resp.country.name or "Unknown"
        iso2 = resp.country.iso_code or "UN"
        iso3 = resp.country.iso_code or "UNK"
        return name, iso2, iso3
    except Exception:
        return "Unknown", "UN", "UNK"


def enrich_geoip(df: pd.DataFrame) -> pd.DataFrame:
    """對 DataFrame 加上 src/dst 國家欄位"""
    df = df.copy()
    df["src_country"], df["src_iso2"], df["src_iso3"] = zip(
        *df["srcip"].map(ip_to_country)
    )
    df["dst_country"], df["dst_iso2"], df["dst_iso3"] = zip(
        *df["dstip"].map(ip_to_country)
    )
    return df
