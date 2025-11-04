# Respondent Data Clean

This repo provides a small, reusable script to join and clean respondent data.

- Inputs: `respondent_contact.csv`, `respondent_other.csv`
- Join key: `respondent_id`
- Output columns (order): `respondent_id, name, address, phone, job, company, birthdate`
- `birthdate`: `MMDDYYYY` -> `YYYY-MM-DD`

## Run
```bash
python respondent_data_clean.py data/respondent_contact.csv data/respondent_other.csv data/respondent_combined.csv
```

## Testing (bonus)
```bash
pip install -r requirements.txt
pytest -q
```
