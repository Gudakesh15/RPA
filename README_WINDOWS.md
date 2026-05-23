# Windows Setup Guide — German Digest Bot

Follow these steps in order on the Windows laptop.

---

## Step 1 — Install Python (if not already installed)

Download from: https://www.python.org/downloads/  
During install: **tick "Add Python to PATH"** before clicking Install.

Verify in Command Prompt:
```
python --version
```

---

## Step 2 — Clone the repository

Open Command Prompt and run:
```
git clone https://github.com/Gudakesh15/RPA.git
cd RPA
```

---

## Step 3 — Create the working folder structure

```
mkdir C:\GermanDigest
mkdir C:\GermanDigest\input
mkdir C:\GermanDigest\output
mkdir C:\GermanDigest\archive
```

---

## Step 4 — Install Python dependencies

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

---

## Step 5 — Copy scripts to working folder

```
xcopy /E /I RPA\GermanDigest\scripts C:\GermanDigest\scripts
```

---

## Step 6 — Test the Python pipeline (without UiPath)

Copy the sample input file to the working folder:
```
copy RPA\GermanDigest\input\sample_raw_searches.xlsx C:\GermanDigest\input\raw_searches.xlsx
```

Then run each script in order:

```
python C:\GermanDigest\scripts\1_extract_words.py
```
Expected output: `Done. 10 unique words written to C:\GermanDigest\input\url_list.txt`

```
python C:\GermanDigest\scripts\2_tar_creator.py
```
Expected output: `Archive saved: C:\GermanDigest\archive\YYYYMMDD_crawl.tar.gz`

```
python C:\GermanDigest\scripts\3_extractor.py
```
Expected output: `Done. X words written to C:\GermanDigest\output\vocabulary_YYYYMMDD.xlsx`

```
python C:\GermanDigest\scripts\4_pdf_generator.py
```
Expected output: `PDF saved: C:\GermanDigest\output\digest_YYYYMMDD.pdf`

Open the PDF in `C:\GermanDigest\output\` to verify.

---

## Step 7 — Install UiPath Studio (if not already installed)

Download from: https://www.uipath.com/start-trial  
Install UiPath Studio Community Edition (free).

---

## Step 8 — Build the UiPath workflow

The UiPath workflow will:
1. Open Chrome and navigate to browser history
2. Filter German-learning URLs
3. Write URLs to `C:\GermanDigest\input\raw_searches.xlsx`
4. Trigger Scripts 1–4 using `Start Process` activity

*(UiPath workflow file will be added to this repo once built.)*

---

## Folder structure reference

```
C:\GermanDigest\
├── input\
│   ├── raw_searches.xlsx       ← UiPath writes here (or paste sample for testing)
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
| `python` not recognised | Re-install Python and tick "Add Python to PATH" |
| `ModuleNotFoundError` | Run `pip install requests beautifulsoup4 pandas openpyxl fpdf2` again |
| Script 2 shows "Possibly blocked" | DWDS rate-limited you — wait 30 seconds and re-run |
| PDF is empty | Check that Script 3 ran successfully and vocabulary Excel has data |
| Git not recognised | Install Git from https://git-scm.com/download/win |
