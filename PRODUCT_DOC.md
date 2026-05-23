# German Browser-to-NotebookLM Learning Digest Bot
### Product Development Document
**Course:** Masters Sem 2 — RPA Seminar  
**Last updated:** 2026-05-23  

---

## HANDOVER — READ THIS FIRST

This document is the single source of truth for the project. If you are starting a new session, read this section first.

### What this project does
A UiPath + Python pipeline that:
1. UiPath opens Chrome → scrapes Google search history from `myactivity.google.com` → writes to Excel
2. Python Script 1 reads that Excel → filters German words → outputs vocabulary list
3. Vocabulary list uploaded to NotebookLM → AI generates audio/video revision overview
4. Optional backup: Python Scripts 2-4 crawl DWDS dictionary, parse HTML, generate PDF

### Where we stopped
- UiPath workflow: **working** — opens Chrome, scrapes history, writes to `raw_searches.xlsx`
- Script 1: **working but needs filter improvement** — correctly parses UiPath output format, identifies German words, but also picks up false positives (addresses with ß, job searches with "germany", words with "meaning" that aren't German)
- Scripts 2-4: **written, tested individually** — DWDS crawler, HTML extractor, PDF generator all work
- Next immediate task: **add `Start Process` in UiPath to trigger Script 1 automatically after writing Excel**

### Key finding from testing
UiPath's `Extract Table Data` on `myactivity.google.com` produces a **single text column** (not URL columns) with entries in this format:
```
Searched for zuständig\n1:28 PM • • Details
Visited https://some-page.com\n2:00 PM • Details
15 cards in your feed\n9:27 PM • Details
```
Script 1 was rewritten to parse this format directly — it does NOT need URLs. It extracts the word from "Searched for [term]" text and builds DWDS URLs itself.

### Known issues to fix
1. **Script 1 false positives** — filter catches addresses with ß (e.g. Chausseestraße), job searches with "germany", and words with "meaning" that aren't German learning searches. Need smarter filtering.
2. **Script 1 only found 1 out of 6 German words** in test — the other 5 German words in history weren't caught. Need to investigate why.
3. **UiPath workflow incomplete** — `Start Process` to trigger Script 1 not yet added.
4. **NotebookLM upload** — not yet built in UiPath.

---

## 1. Problem Statement

Non-native German learners search words throughout the day (on Google, Duden, DeepL, Linguee, DWDS, Reverso) but lose those learning moments in browser history. The goal is to automate the collection of those searches and turn them into structured, revisable learning material — including AI-generated audio and video overviews via NotebookLM.

---

## 2. Solution Overview

UiPath-orchestrated pipeline:
1. UiPath scrapes Chrome history → Excel
2. Python extracts German words → vocabulary Excel
3. UiPath uploads vocabulary to NotebookLM → AI revision overview
4. Backup: Python crawls DWDS + generates PDF

**Key insight:** Google account sync means Chrome history on desktop includes searches from phone/tablet on the same Google account. UiPath targets `myactivity.google.com/product/search?hl=en` (Google Search activity only).

---

## 3. Architecture Decision Log

| Decision | Chosen approach | Why |
|---|---|---|
| Browser input | `myactivity.google.com/product/search?hl=en` | Cross-device via Google sync; regular web page UiPath can scrape |
| UiPath activity | `Use Application/Browser` + `Extract Table Data` | Captures search history as text entries |
| Data format from UiPath | Single text column: "Searched for [term]" | What Extract Table Data actually produces on this page |
| Word extraction | Parse "Searched for [term]" text directly | No URLs needed — word is in the text |
| German detection | German characters (ä,ö,ü,ß) OR learning keywords | Simple heuristic, works for most cases |
| Enrichment source | DWDS (`dwds.de`) | Scraper-friendly German dictionary |
| Primary output | NotebookLM | Richer AI revision than static PDF |
| Backup output | PDF via `fpdf2` | For demo/presentation purposes |
| Platform | Windows laptop | UiPath runs on Windows |
| IDE | VS Code with integrated terminal | Team preference |

---

## 4. Pipeline

### Primary (NotebookLM)
```
[Chrome — myactivity.google.com/product/search?hl=en]
        |
        v
[UiPath: Use Application/Browser]
  - Extract Table Data → single column "Searched for [term]" entries
  - Use Excel File → Write Data Table to Sheet
        |
        v
[GermanDigest/input/raw_searches.xlsx]  ← UiPath writes here
        |
        v
[Script 1: 1_extract_words.py]  ← UiPath triggers via Start Process
  - Reads first column of raw_searches.xlsx
  - Filters "Searched for" entries only
  - Detects German by ä/ö/ü/ß characters or learning keywords
  - Deduplicates
  - Writes: input/url_list.txt (for DWDS crawl)
  - Writes: output/vocabulary_words.xlsx (for NotebookLM)
        |
        v
[UiPath: uploads vocabulary_words.xlsx to notebooklm.google.com]
        |
        v
[NotebookLM → audio overview, quiz, summary]
```

### Backup (PDF)
```
[output/vocabulary_words.xlsx]
  → Script 2: crawl DWDS → TAR archive
  → Script 3: parse HTML → enriched Excel
  → Script 4: generate PDF digest
```

---

## 5. Folder Structure

```
RPA/  (repo root — cloned to Windows laptop)
├── GermanDigest/
│   ├── input/
│   │   ├── raw_searches.xlsx       ← UiPath writes here (gitignored)
│   │   ├── url_list.txt            ← Script 1 writes here (gitignored)
│   │   └── sample_raw_searches.xlsx ← test input (committed)
│   ├── output/
│   │   ├── vocabulary_words.xlsx   ← Script 1 main output
│   │   ├── vocabulary_YYYYMMDD.xlsx ← Script 3 enriched output
│   │   └── digest_YYYYMMDD.pdf     ← Script 4 output
│   ├── archive/
│   │   └── YYYYMMDD_crawl.tar.gz  ← Script 2 output
│   └── scripts/
│       ├── 1_extract_words.py      ← rewritten for UiPath output format
│       ├── 2_tar_creator.py
│       ├── 3_extractor.py
│       └── 4_pdf_generator.py
├── Avi's Crawler/                  ← original reference scripts
├── UiPath/GermanDigestBot/         ← UiPath project folder
│   └── Main.xaml                   ← UiPath workflow
├── PRODUCT_DOC.md                  ← this file
└── README.md                       ← Windows setup guide

GitHub: https://github.com/Gudakesh15/RPA
```

---

## 6. UiPath Workflow — Current State

**Built so far (Main.xaml):**
```
Main Sequence
  └── Use Application/Browser (Chrome - myactivity.google.com/product/search?hl=en)
        └── Do
              ├── Delay (00:00:05)
              └── Extract Table Data → dtSearchHistory
                  [linked to Use Excel File below]

  └── Use Excel File (raw_searches.xlsx)
        └── Do
              └── Write Data Table to Sheet (dtSearchHistory → RawSearches, A1)
```

**Still to build:**
```
  └── Start Process
        FileName: python
        Arguments: "[full path]\GermanDigest\scripts\1_extract_words.py"

  └── [Later] Use Application/Browser (notebooklm.google.com)
        └── Upload vocabulary_words.xlsx
```

---

## 7. File Index

| File | Purpose | Status |
|---|---|---|
| `GermanDigest/scripts/1_extract_words.py` | Parse UiPath output → extract German words → vocabulary Excel | Done, needs filter improvement |
| `GermanDigest/scripts/2_tar_creator.py` | Crawl DWDS → TAR archive | Done |
| `GermanDigest/scripts/3_extractor.py` | Parse TAR → enriched vocabulary Excel | Done |
| `GermanDigest/scripts/4_pdf_generator.py` | Vocabulary Excel → PDF | Done |
| `GermanDigest/input/sample_raw_searches.xlsx` | Test input file | Done |
| `UiPath/GermanDigestBot/Main.xaml` | UiPath workflow | Partial — missing Start Process + NotebookLM |
| `Avi's Crawler/` | Original reference scripts | Existing |

---

## 8. Python Dependencies

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

---

## 9. Progress Tracker

| Task | Status |
|---|---|
| Project architecture defined | Done |
| GitHub repo set up | Done |
| Script 1: extract_words.py | Done (needs filter fix) |
| Script 2: tar_creator.py | Done |
| Script 3: extractor.py | Done |
| Script 4: pdf_generator.py | Done |
| Sample test input created | Done |
| UiPath: open Chrome + navigate to myactivity | Done |
| UiPath: Extract Table Data → raw_searches.xlsx | Done |
| UiPath: Start Process → trigger Script 1 | To do (next) |
| Script 1: improve German word filter | To do |
| UiPath: NotebookLM upload | To do |
| End-to-end test | To do |
| Presentation slides | To do |
| Final report | To do |

---

## 10. Immediate Next Steps (pick up here)

1. **Add `Start Process` in UiPath** after the Excel write step:
   - FileName: `python`
   - Arguments: full path to `1_extract_words.py`

2. **Fix Script 1 filter** — improve German word detection to reduce false positives:
   - Exclude entries containing numbers (addresses)
   - Require German characters OR German dictionary keywords (not just "meaning" or "germany" as standalone job search words)
   - Investigate why only 1 of 6 German words was detected in test

3. **Build NotebookLM upload in UiPath**

4. **End-to-end test** of full pipeline

---

## 11. Presentation Outline (draft)

1. **Problem** — what learners lose every day
2. **Solution overview** — the two-path pipeline diagram
3. **Live demo** — run the bot: browser → vocabulary Excel → NotebookLM
4. **Technical deep dive** — BPMN, web scraping, TAR archiving, BeautifulSoup (backup path as evidence of technical work)
5. **Key decisions** — why NotebookLM over PDF, why Google sync, why UiPath + Python
6. **Results** — NotebookLM audio overview of the week's German words
7. **Limitations and future work** — scheduling, LLM enrichment, Anki export

---

## 12. Team Work Division

| Person | Responsibility |
|---|---|
| Person 1 (Rodrigo) | UiPath workflow — browser scraping + Excel write + Script 1 trigger |
| Person 2 | UiPath NotebookLM upload + end-to-end testing |
| Person 3 (Avi) | Python scripts + PDF backup demo + filter improvement |

---

*This document is updated continuously. Last session ended: 2026-05-23.*
