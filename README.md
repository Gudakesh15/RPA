# German Digest Bot — Setup & Run Guide

## Prerequisites (already done)
- Python installed
- UiPath Studio installed and linked to university account
- Git installed
- VS Code installed

---

## Step 1 — Clone the repository

Open **VS Code**, then open the integrated terminal with `` Ctrl+` `` and run:
```
git clone https://github.com/Gudakesh15/RPA.git
```

Then open the cloned folder in VS Code: **File → Open Folder → select the `RPA` folder**.

---

## Step 2 — Create the output folders

The `GermanDigest` folder is already in the repo. You just need to create the subfolders that git doesn't track. In the VS Code integrated terminal (`` Ctrl+` ``):
```
mkdir GermanDigest\output
mkdir GermanDigest\archive
```

---

## Step 3 — Install Python dependencies

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

---

## Step 4 — Test the Python pipeline (without UiPath)

Copy the sample input file so Script 1 can find it:
```
cp GermanDigest\input\sample_raw_searches.xlsx GermanDigest\input\raw_searches.xlsx
```

Run each script in order from the VS Code terminal:

```
python GermanDigest\scripts\1_extract_words.py
```
Expected: `Done. 10 unique words written to ...GermanDigest\input\url_list.txt`

```
python GermanDigest\scripts\2_tar_creator.py
```
Expected: `Archive saved: ...GermanDigest\archive\YYYYMMDD_crawl.tar.gz`

```
python GermanDigest\scripts\3_extractor.py
```
Expected: `Done. X words written to ...GermanDigest\output\vocabulary_YYYYMMDD.xlsx`

```
python GermanDigest\scripts\4_pdf_generator.py
```
Expected: `PDF saved: ...GermanDigest\output\digest_YYYYMMDD.pdf`

Open the PDF in `GermanDigest\output\` to verify the vocabulary cards.

---

## Step 5 — Build the UiPath workflow

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
