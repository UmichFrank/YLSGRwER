from __future__ import annotations
import csv, subprocess, sys
from pathlib import Path

def write_csv(path: Path, rows: list[dict[str,str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rows[0].keys())
        w.writeheader(); w.writerows(rows)

def test_end_to_end(tmp_path: Path) -> None:
    c = tmp_path / "contact.csv"
    o = tmp_path / "other.csv"
    out = tmp_path / "combined.csv"
    write_csv(c, [
        {"respondent_id":"1","name":"Alice","address":"A St\nCity","phone":"123"},
        {"respondent_id":"2","name":"Bob","address":"B St\nCity","phone":"456"},
    ])
    write_csv(o, [
        {"respondent_id":"1","job":"Dev","company":"Acme","birthdate":"01021990"},
        {"respondent_id":"2","job":"PM","company":"Beta","birthdate":"12311999"},
    ])
    cmd = [sys.executable, str(Path(__file__).resolve().parents[1]/"respondent_data_clean.py"),
           str(c), str(o), str(out)]
    subprocess.run(cmd, check=True)
    lines = out.read_text(encoding="utf-8").splitlines()
    assert lines[0].split(',')[:7] == ["respondent_id","name","address","phone","job","company","birthdate"]
    assert lines[1].endswith("1990-01-02")
