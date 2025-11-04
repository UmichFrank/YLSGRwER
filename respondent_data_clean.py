#!/usr/bin/env python3
"""
Join respondent_contact.csv and respondent_other.csv on respondent_id,
write combined CSV with columns (order strict):
respondent_id, name, address, phone, job, company, birthdate
birthdate: MMDDYYYY -> YYYY-MM-DD

Usage:
    python respondent_data_clean.py <contact_info_file> <other_info_file> <output_file>
"""
from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional
import pandas as pd

REQUIRED_COLUMNS = ["respondent_id","name","address","phone","job","company","birthdate"]

def _fmt_birthdate(series: pd.Series) -> pd.Series:
    """MMDDYYYY -> YYYY-MM-DD; invalid -> empty string."""
    def conv(v: Optional[str]) -> str:
        if v is None or pd.isna(v): return ""
        s = str(v).strip()
        if len(s)==8 and s.isdigit():
            mm, dd, yyyy = s[:2], s[2:4], s[4:]
            return f"{yyyy}-{mm}-{dd}"
        return ""
    return series.apply(conv)

def main(argv: list[str] | None = None) -> None:
    p = argparse.ArgumentParser("respondent cleaner")
    p.add_argument("contact_info_file", help="Path to respondent_contact.csv")
    p.add_argument("other_info_file",   help="Path to respondent_other.csv")
    p.add_argument("output_file",       help="Path to output combined CSV")
    args = p.parse_args(argv)

    contact = Path(args.contact_info_file)
    other   = Path(args.other_info_file)
    out     = Path(args.output_file)
    out.parent.mkdir(parents=True, exist_ok=True)

    cdf = pd.read_csv(contact, dtype=str, keep_default_na=False)
    odf = pd.read_csv(other,   dtype=str, keep_default_na=False)

    merged = cdf.merge(odf, on="respondent_id", how="inner", sort=False)

    for col in merged.columns:
        merged[col] = merged[col].astype(str).str.strip()

    if "birthdate" in merged.columns:
        merged["birthdate"] = _fmt_birthdate(merged["birthdate"])

    missing = [c for c in REQUIRED_COLUMNS if c not in merged.columns]
    if missing:
        raise SystemExit(f"Missing columns after merge: {missing}")

    merged = merged[REQUIRED_COLUMNS]
    merged.to_csv(out, index=False)
    print(f"Wrote -> {out}")

if __name__ == "__main__":
    main()
