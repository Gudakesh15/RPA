# German Browser-to-PDF Learning Digest Bot
### Product Development Document
**Course:** Masters Sem 2 — RPA Seminar  
**Last updated:** 2026-05-23  

---

## 1. Problem Statement

Non-native German learners search words throughout the day (on Google, Duden, DeepL, Linguee, DWDS, Reverso) but lose those learning moments in browser history. The goal is to automate the collection of those searches and turn them into structured, revisable learning material.

---

## 2. Solution Overview

A UiPath-orchestrated RPA pipeline that:
1. Reads German vocabulary searches from Chrome browser history
2. Extracts and deduplicates the searched words
3. Crawls dictionary pages (DWDS) to get meanings and examples
4. Generates a PDF learning digest

**Key insight:** Google account sync means Chrome history on the desktop includes searches made on any device (phone, tablet) logged into the same account. UiPath targets `myactivity.google.com` or Chrome history to collect these cross-device searches.

---

## 3. Architecture Decision Log

| Decision | Chosen approach | Why |
|---|---|---|
| Browser input method | Chrome history via UiPath browser automation | Cross-device via Google sync; avoids manual Excel input |
| History source | `myactivity.google.com` (preferred) or `chrome://history` | Regular web page, more UiPath-friendly than `chrome://` internal pages |
| Word enrichment source | DWDS (`dwds.de`) | More scraper-friendly than Duden; reliable German dictionary |
| Scraping infrastructure | Adapted from existing `Avi's Crawler` Python scripts | TAR-based HTML archiving + BeautifulSoup parsing already proven |
| Orchestration | UiPath triggers Python scripts via `Start Process` activity | UiPath handles browser + file I/O; Python handles crawling + PDF |
| PDF generation | Python `fpdf2` library | Lightweight, no external dependencies, UiPath-triggerable |
| Platform | Windows laptop | UiPath runs natively on Windows |

---

## 4. MVP Scope

**In scope:**
- UiPath reads Chrome history → writes URLs to Excel
- Python extracts German words from URLs, deduplicates, builds DWDS lookup URLs
- Python crawls DWDS pages, archives HTML (TAR)
- Python parses HTML, extracts meanings + examples → vocabulary Excel
- Python generates PDF digest

**Out of scope for MVP:**
- NotebookLM upload (manual step if desired)
- LLM-generated enrichment (template-based for now)
- Automatic scheduling (manual trigger)
- Anki/flashcard export

---

## 5. Pipeline

```
[Chrome Browser History]
        |
        v
[UiPath] — scrapes history page, filters German-learning URLs
        |
        v
[input/raw_searches.xlsx] — columns: url, page_title, timestamp
        |
        v
[Script 1: 1_extract_words.py]
  - parses query strings (Google, DeepL, Duden, DWDS, Linguee, Reverso)
  - strips filler words: meaning, translation, bedeutung, deutsch...
  - deduplicates
  - builds DWDS lookup URLs
  - writes: input/url_list.txt
        |
        v
[Script 2: 2_tar_creator.py]
  - reads url_list.txt
  - crawls each DWDS page with session + user-agent rotation
  - archives HTML to: archive/YYYYMMDD_crawl.tar.gz
        |
        v
[Script 3: 3_extractor.py]
  - opens TAR archive
  - parses each DWDS page with BeautifulSoup
  - extracts: word, meaning, example sentence, usage note, source URL
  - writes: output/vocabulary_YYYYMMDD.xlsx
        |
        v
[Script 4: 4_pdf_generator.py]
  - reads vocabulary Excel
  - generates structured PDF with word cards
  - writes: output/digest_YYYYMMDD.pdf
        |
        v
[PDF Digest] — ready for revision / optional NotebookLM upload
```

---

## 6. Folder Structure (Windows)

```
C:\GermanDigest\
├── input\
│   ├── raw_searches.xlsx       ← UiPath writes here
│   └── url_list.txt            ← Script 1 writes here
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

## 7. File Index

| File | Purpose | Status |
|---|---|---|
| `GermanDigest/scripts/1_extract_words.py` | Parse URLs → extract German words → build DWDS URLs | Done |
| `GermanDigest/scripts/2_tar_creator.py` | Crawl DWDS pages → save HTML to TAR archive | Done |
| `GermanDigest/scripts/3_extractor.py` | Parse TAR archive → extract vocabulary → Excel | Done |
| `GermanDigest/scripts/4_pdf_generator.py` | Vocabulary Excel → PDF digest | Done |
| `Avi's Crawler/Aviral.py` | Original HTTP crawler (source reference) | Existing |
| `Avi's Crawler/1_TarFileCreator.py` | Original TAR creator (source reference) | Existing |
| `Avi's Crawler/2_Dormeo Information extractor.py` | Original HTML extractor (source reference) | Existing |
| `Avi's Crawler/3_PushDataToSQL (dormeo).py` | Original SQL pusher (source reference) | Existing |
| UiPath workflow | Browser automation — scrape history → write Excel | To do |

---

## 8. Python Dependencies (install on Windows laptop)

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

---

## 9. UiPath Workflow — To Build

The UiPath workflow needs to:

1. **Open Chrome** and navigate to `myactivity.google.com` (or `chrome://history`)
2. **Scrape entries** — extract URL and page title from each history item
3. **Filter** — keep only entries matching German-learning keywords:
   - `meaning`, `bedeutung`, `übersetzung`, `translation`, `duden`, `dwds`, `linguee`, `reverso`, `deepl`, `was bedeutet`, `synonym`
4. **Write to Excel** — save filtered URLs to `C:\GermanDigest\input\raw_searches.xlsx`
5. **Trigger Script 1** — `Start Process: python C:\GermanDigest\scripts\1_extract_words.py`
6. **Trigger Script 2** — `Start Process: python C:\GermanDigest\scripts\2_tar_creator.py`
7. **Trigger Script 3** — `Start Process: python C:\GermanDigest\scripts\3_extractor.py`
8. **Trigger Script 4** — `Start Process: python C:\GermanDigest\scripts\4_pdf_generator.py`
9. **Open output folder** — show the user the generated PDF

---

## 10. Risks and Mitigations

| Risk | Mitigation |
|---|---|
| `myactivity.google.com` layout changes break UiPath selectors | Add fallback: manual URL paste into `raw_searches.xlsx` |
| DWDS blocks scraper | User-agent rotation + retry logic already built into Script 2 |
| DWDS HTML structure changes break BeautifulSoup selectors | CSS class patterns use `re.compile` for partial match flexibility |
| UiPath Chrome extension can't access `chrome://` pages | Use `myactivity.google.com` instead |
| PDF fonts/layout issues on Windows | `fpdf2` uses built-in Helvetica — no external font files needed |

---

## 11. Team Work Division

| Person | Responsibility |
|---|---|
| Person 1 | UiPath workflow — browser history scraping + Excel output + script triggers |
| Person 2 | Python Scripts 1–3 — word extraction, TAR crawling, HTML parsing |
| Person 3 | Python Script 4 — PDF generation + testing end-to-end pipeline |

---

## 12. Next Steps

- [ ] Build UiPath workflow (browser → Excel → trigger scripts)
- [ ] Test Script 1 with a sample `raw_searches.xlsx` (10 real German search URLs)
- [ ] Test Script 2 crawling DWDS and verify HTML archive is created
- [ ] Verify Script 3 BeautifulSoup selectors against live DWDS HTML
- [ ] Test Script 4 PDF output formatting
- [ ] End-to-end test on Windows laptop
- [ ] Initialize GitHub repo and push all files
- [ ] Prepare presentation slides
- [ ] Write final report

---

## 13. Presentation Outline (draft)

1. Problem — what learners lose every day
2. Solution overview — the pipeline
3. Demo — run the bot live (or recorded)
4. Architecture — BPMN diagram
5. Key technical decisions — why UiPath + Python, why DWDS, why TAR
6. Results — sample PDF digest
7. Limitations and future work (NotebookLM, LLM enrichment, scheduling)

---

*This document is updated continuously as the project develops.*
