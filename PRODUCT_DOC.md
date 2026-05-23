# German Browser-to-NotebookLM Learning Digest Bot
### Product Development Document
**Course:** Masters Sem 2 — RPA Seminar  
**Last updated:** 2026-05-23  

---

## 1. Problem Statement

Non-native German learners search words throughout the day (on Google, Duden, DeepL, Linguee, DWDS, Reverso) but lose those learning moments in browser history. The goal is to automate the collection of those searches and turn them into structured, revisable learning material — including AI-generated audio and video overviews.

---

## 2. Solution Overview

A UiPath-orchestrated RPA pipeline that:
1. Reads German vocabulary searches from Chrome browser history
2. Extracts and deduplicates the searched words
3. Produces a clean vocabulary list
4. Uploads the list to NotebookLM, which generates an AI-powered audio/video revision overview

**Key insight:** Google account sync means Chrome history on the desktop includes searches made on any device (phone, tablet). UiPath targets `myactivity.google.com` or `chrome://history` to collect these cross-device searches automatically.

**Why NotebookLM over PDF:** NotebookLM is an AI — it understands the German words from the vocabulary list without needing explicit meanings pre-scraped. It generates richer revision material (audio overviews, quizzes, summaries) than a static PDF, and the upload can be automated by UiPath. This removes the need for web scraping dictionary pages entirely.

---

## 3. Architecture Decision Log

| Decision | Chosen approach | Why |
|---|---|---|
| Browser input method | Chrome history via UiPath browser automation | Cross-device via Google sync; no manual input |
| History source | `myactivity.google.com` (preferred) or `chrome://history` | Regular web page, UiPath-friendly |
| Output destination | NotebookLM (primary) + PDF (backup/demo) | NotebookLM gives richer AI revision; PDF kept for demo purposes |
| Word enrichment | Not required for NotebookLM path | NotebookLM understands words directly from the vocabulary list |
| Python scraping scripts | Kept as optional/demo path | Scripts 2–3 (TAR + DWDS) shown as technical depth; not needed for main flow |
| Orchestration | UiPath triggers Python + automates NotebookLM upload | UiPath handles full pipeline end to end |
| Platform | Windows laptop | UiPath runs natively on Windows |

---

## 4. MVP Scope

### Primary pipeline (NotebookLM path)
- UiPath scrapes Chrome history → filters German-learning URLs → writes to Excel
- Python Script 1 extracts and deduplicates German words → vocabulary Excel
- UiPath uploads vocabulary Excel to NotebookLM
- NotebookLM generates audio overview, quiz, and summary

### Backup / demo pipeline (PDF path)
- Python Scripts 2–4 crawl DWDS, parse HTML, generate PDF
- Shown in presentation as technical depth — demonstrates web scraping, TAR archiving, BeautifulSoup parsing, PDF generation

**Out of scope for MVP:**
- Automatic scheduling (manual trigger for now)
- Anki/flashcard export
- LLM API enrichment

---

## 5. Pipeline

### Primary (NotebookLM)
```
[Chrome Browser History — synced across all devices via Google account]
        |
        v
[UiPath] — opens myactivity.google.com, filters German-learning URLs
        |
        v
[GermanDigest/input/raw_searches.xlsx]
  columns: url, page_title, timestamp
        |
        v
[Script 1: 1_extract_words.py]
  - parses query strings (Google, DeepL, Duden, Linguee, Reverso)
  - strips filler words: meaning, translation, bedeutung, deutsch...
  - deduplicates
  - writes: output/vocabulary_YYYYMMDD.xlsx
        |
        v
[UiPath] — opens notebooklm.google.com, uploads vocabulary Excel
        |
        v
[NotebookLM] — AI generates audio overview, quiz, summary, flashcards
```

### Backup (PDF)
```
[output/vocabulary_YYYYMMDD.xlsx]
        |
        v
[Script 2: 2_tar_creator.py] — crawls DWDS pages → TAR archive
        |
        v
[Script 3: 3_extractor.py] — parses HTML → enriched vocabulary Excel
        |
        v
[Script 4: 4_pdf_generator.py] — generates PDF digest
        |
        v
[output/digest_YYYYMMDD.pdf]
```

---

## 6. Folder Structure

```
RPA/
└── GermanDigest/
    ├── input/
    │   ├── raw_searches.xlsx       ← UiPath writes here
    │   └── url_list.txt            ← Script 1 writes here (backup path only)
    ├── output/
    │   ├── vocabulary_YYYYMMDD.xlsx  ← main output, uploaded to NotebookLM
    │   └── digest_YYYYMMDD.pdf       ← backup PDF output
    ├── archive/
    │   └── YYYYMMDD_crawl.tar.gz   ← backup path only
    └── scripts/
        ├── 1_extract_words.py
        ├── 2_tar_creator.py        ← backup/demo
        ├── 3_extractor.py          ← backup/demo
        └── 4_pdf_generator.py      ← backup/demo
```

---

## 7. File Index

| File | Purpose | Status |
|---|---|---|
| `GermanDigest/scripts/1_extract_words.py` | Parse URLs → extract German words → vocabulary Excel | Done |
| `GermanDigest/scripts/2_tar_creator.py` | Crawl DWDS pages → TAR archive (backup/demo) | Done |
| `GermanDigest/scripts/3_extractor.py` | Parse TAR → enriched vocabulary Excel (backup/demo) | Done |
| `GermanDigest/scripts/4_pdf_generator.py` | Vocabulary Excel → PDF digest (backup/demo) | Done |
| `GermanDigest/input/sample_raw_searches.xlsx` | Test input — 10 German search URLs + 2 irrelevant | Done |
| `Avi's Crawler/` | Original crawler scripts — source reference for adaptation | Existing |
| UiPath workflow | Browser scraping + Script 1 trigger + NotebookLM upload | To do |

---

## 8. Python Dependencies

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

---

## 9. UiPath Workflow — To Build

### Part A: Input collection
1. Open Chrome → navigate to `myactivity.google.com`
2. Scrape history entries (URL + page title)
3. Filter for German-learning keywords: `meaning`, `bedeutung`, `übersetzung`, `translation`, `duden`, `dwds`, `linguee`, `reverso`, `deepl`, `was bedeutet`, `synonym`
4. Write filtered URLs to `GermanDigest/input/raw_searches.xlsx`

### Part B: Word extraction
5. Trigger Script 1 via `Start Process`: `python GermanDigest\scripts\1_extract_words.py`
6. Wait for script to complete

### Part C: NotebookLM upload
7. Open Chrome → navigate to `notebooklm.google.com`
8. Create new notebook or open existing
9. Upload `GermanDigest/output/vocabulary_YYYYMMDD.xlsx`
10. Wait for NotebookLM to process
11. Optionally trigger audio overview generation

---

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| `myactivity.google.com` layout changes break selectors | Fallback: user pastes URLs manually into `raw_searches.xlsx` |
| NotebookLM UI changes break UiPath selectors | Manual upload as fallback — still demonstrates the concept |
| UiPath Chrome extension blocked on `chrome://` pages | Use `myactivity.google.com` instead |
| DWDS selectors break (backup path) | Backup path is demo only — not critical for main flow |

---

## 11. Team Work Division

| Person | Responsibility |
|---|---|
| Person 1 | UiPath Part A — browser history scraping + Excel output |
| Person 2 | UiPath Part B+C — trigger Script 1 + NotebookLM upload automation |
| Person 3 | Python scripts + PDF backup demo + end-to-end testing |

---

## 12. Progress Tracker

| Task | Status |
|---|---|
| Project architecture defined | Done |
| GitHub repo set up | Done |
| Script 1: extract_words.py | Done |
| Script 2: tar_creator.py | Done |
| Script 3: extractor.py | Done |
| Script 4: pdf_generator.py | Done |
| Sample test input created | Done |
| Scripts tested on Windows (pipeline validated) | In progress |
| UiPath workflow — Part A (browser scraping) | To do |
| UiPath workflow — Part B (trigger Script 1) | To do |
| UiPath workflow — Part C (NotebookLM upload) | To do |
| End-to-end test | To do |
| Presentation slides | To do |
| Final report | To do |

---

## 13. Presentation Outline (draft)

1. **Problem** — what learners lose every day
2. **Solution overview** — the two-path pipeline
3. **Live demo** — run the bot: browser → vocabulary Excel → NotebookLM
4. **Technical deep dive** — BPMN diagram, web scraping, TAR archiving, BeautifulSoup (backup path as evidence of technical work)
5. **Key decisions** — why NotebookLM over PDF, why Google sync, why UiPath + Python
6. **Results** — NotebookLM audio overview of the week's German words
7. **Limitations and future work** — scheduling, LLM enrichment, Anki export

---

*This document is updated continuously as the project develops.*
