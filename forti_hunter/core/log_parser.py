import pandas as pd
import re

def parse_fortigate_rawlog(log_file):
    """
    解析 FortiGate Raw Log（key=value 格式）
    """
    rows = []
    with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            kv = dict(re.findall(r'(\w+)=(".*?"|\S+)', line))

            # 移除引號
            for k, v in kv.items():
                if isinstance(v, str) and v.startswith('"') and v.endswith('"'):
                    kv[k] = v[1:-1]

            rows.append(kv)

    return pd.DataFrame(rows)


def load_blacklist(path):
    """
    載入 IP 黑名單
    """
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return { x.strip() for x in f.readlines() if x.strip() }
