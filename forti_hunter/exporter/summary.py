import os

def export_summary(stats, all_df, matched, output_dir, output_files):

    fpath = os.path.join(output_dir, "summary.txt")

    with open(fpath, "w", encoding="utf-8") as f:
        f.write("=== FortiGate Threat Summary ===\n\n")
        f.write(f"Total logs       : {len(all_df):,}\n")
        f.write(f"Matched (malicious): {len(matched):,}\n\n")

        f.write("Top Source Countries:\n")
        df = stats["src_country_counts_df"].head(10)
        for _, row in df.iterrows():
            f.write(f" - {row['country_iso2']}: {row['count']}\n")

    output_files.append(fpath)
