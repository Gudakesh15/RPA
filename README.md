# German Digest Bot — Setup & Run Guide

## Prerequisites (already done)
- Python installed
- UiPath Studio installed and linked to university account
- Git installed

---

## Step 1 — Clone the repository

Open **Terminal** and run:
```
git clone https://github.com/Gudakesh15/RPA.git
```

---

## Step 2 — Create the working folder structure

In Terminal:
```
mkdir C:\GermanDigest
mkdir C:\GermanDigest\input
mkdir C:\GermanDigest\output
mkdir C:\GermanDigest\archive
mkdir C:\GermanDigest\scripts
```

---

## Step 3 — Copy scripts to the working folder

```
cp -r RPA\GermanDigest\scripts\* C:\GermanDigest\scripts\
```

---

## Step 4 — Install Python dependencies

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

---

## Step 5 — Test the Python pipeline (without UiPath)

Copy the sample input file:
```
cp RPA\GermanDigest\input\sample_raw_searches.xlsx C:\GermanDigest\input\raw_searches.xlsx
```

Run each script in order:

```
python C:\GermanDigest\scripts\1_extract_words.py
```
Expected: `Done. 10 unique words written to C:\GermanDigest\input\url_list.txt`

```
python C:\GermanDigest\scripts\2_tar_creator.py
```
Expected: `Archive saved: C:\GermanDigest\archive\YYYYMMDD_crawl.tar.gz`

```
python C:\GermanDigest\scripts\3_extractor.py
```
Expected: `Done. X words written to C:\GermanDigest\output\vocabulary_YYYYMMDD.xlsx`

```
python C:\GermanDigest\scripts\4_pdf_generator.py
```
Expected: `PDF saved: C:\GermanDigest\output\digest_YYYYMMDD.pdf`

Open the PDF in `C:\GermanDigest\output\` to verify the vocabulary cards.

---

## Step 6 — Build the UiPath workflow

Open UiPath Studio and create a new project. The workflow will:
1. Open Chrome and navigate to browser history
2. Filter for German-learning URLs
3. Write URLs to `C:\GermanDigest\input\raw_searches.xlsx`
4. Trigger Scripts 1–4 using the `Start Process` activity

*(UiPath workflow .xaml file will be added to this repo once built.)*

---

## Folder structure reference

```
C:\GermanDigest\
├── input\
│   ├── raw_searches.xlsx       ← UiPath writes here
│   └── url_list.txt            ← Script 1 writes here automatically
├── output\
│   ├── vocabulary_YYYYMMDD.xlsx
│   └── digest_YYYYMMDD.pdf
├── archive\
│   └── YYYYMMDD_crawl.tar.gz
└── scripts\
    ├── 1_extract_words.py
    ├── 2_tar_creator.py
    ├── 3_extractor.py
    └── 4_pdf_generator.py
```

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `ModuleNotFoundError` | Run `pip install requests beautifulsoup4 pandas openpyxl fpdf2` |
| Script 2 shows "Possibly blocked" | DWDS rate-limited — wait 30 seconds and re-run |
| PDF is empty | Check Script 3 ran successfully and vocabulary Excel has data |
