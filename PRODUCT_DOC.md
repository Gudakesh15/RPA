# German Browser-to-NotebookLM Learning Digest Bot
### Product Development Document
**Course:** Masters Sem 2 — RPA Seminar  
**Last updated:** 2026-05-23 (Session 2 — MVP Complete)

---

## HANDOVER — READ THIS FIRST

This document is the single source of truth for the project. If you are starting a new session, read this section first.

### Current status: MVP IS COMPLETE ✓

The full pipeline runs end-to-end and has been demonstrated:
1. UiPath opens Chrome → scrapes Google search history → writes to Excel ✓
2. UiPath triggers Python Script 1 → filters German words → writes vocabulary files ✓
3. UiPath opens NotebookLM → creates new notebook → uploads vocabulary source file ✓
4. UiPath triggers Video Overview → enters custom prompt → generates AI video ✓
5. UiPath shows "Process completed" message box ✓

A recording of the full working flow was captured in Session 2.

### What the UiPath workflow does (Main.xaml — complete)

```
Use Application/Browser (Chrome — myactivity.google.com/product/search?hl=en)
  └── Do
        ├── Delay (5s)
        ├── Extract Table Data → dtSearchHistory
        ├── Use Excel File (raw_searches.xlsx)
        │     └── Write DataTable to Sheet (RawSearches)
        ├── Start Process
        │     FileName: C:\Python313\python.exe
        │     Arguments: Chr(34) & "[path]\1_extract_words.py" & Chr(34)
        ├── Delay (30s)  ← waits for Script 1 to finish
        ├── Go To URL → https://notebooklm.google.com/
        ├── Click 'SPAN(1)' → New notebook button
        ├── Delay (5s)
        ├── Click 'SPAN(2)' → Upload file (in add-sources-dialog)
        ├── Delay (2s)
        ├── Type Into → file path in Windows Open dialog
        │     Text: [path]\GermanDigest\output\notebooklm_source.txt
        ├── Click 'Open' → confirms Windows file picker
        ├── Delay (10s)  ← waits for upload to process
        ├── Click 'chevron_forward' → Video Overview button (studio panel)
        ├── Delay (4s)
        ├── Mouse Scroll → scrolls MAT-DIALOG-CONTENT down
        ├── Delay (5s)
        ├── Click 'TEXTAREA' (idx='3') → custom prompt text box
        ├── Type Into → custom prompt text
        ├── Click 'SPAN(3)' → Generar/Generate button (fuzzy selector)
        ├── Delay (5s)
        └── Message Box → "Process completed"
```

### Python scripts — current state

| Script | Status | Output |
|--------|--------|--------|
| `1_extract_words.py` | Working — filter needs improvement | `vocabulary_words.xlsx`, `notebooklm_source.txt`, `url_list.txt` |
| `2_tar_creator.py` | Done | `archive/YYYYMMDD_crawl.tar.gz` |
| `3_extractor.py` | Done | `output/vocabulary_YYYYMMDD.xlsx` |
| `4_pdf_generator.py` | Done | `output/digest_YYYYMMDD.pdf` |

### Key technical discoveries (from testing)

1. **UiPath data format:** `myactivity.google.com` produces a single text column with entries like `"Searched for zuständig\n1:28 PM • • Details"` — not URL columns. Script 1 parses this format directly.

2. **Python path:** Use `C:\Python313\python.exe` (full path, not just `python`). Paths with spaces need `Chr(34)` quoting in UiPath Arguments field.

3. **NotebookLM dynamic IDs:** Angular Material assigns IDs like `mat-input-0`, `mat-input-1` dynamically each page load. Fixed by using `idx='3'` in the TEXTAREA selector instead of the ID.

4. **NotebookLM language:** The Generate button is labelled "Generar" (Spanish UI). A fuzzy selector targets `aaname=' Generar '`.

5. **One browser session:** The entire UiPath workflow runs inside a single `Use Application/Browser` block. `Go To URL` navigates the same Chrome window from Google My Activity to NotebookLM — no second browser block needed.

### Known issues to fix in next session

1. **Script 1 false positives** — catches addresses with ß (Chausseestraße), job searches with "germany", non-German words with "meaning". Only 1 of 6 German words detected in first test. Filter logic needs improvement.
2. **Hardcoded notebook URL** — the TEXTAREA click selector references a specific notebook URL (`/notebook/09a77e80...`). If that notebook is deleted or a new one is created at a different URL, the selector may not fire. Should be re-indicated against the freshly created notebook.
3. **No conditional logic** — if Script 1 finds 0 German words, the workflow still tries to upload an empty file to NotebookLM. Should add an `If` gate.

---

## 1. Problem Statement

Non-native German learners search words throughout the day (on Google, Duden, DeepL, Linguee, DWDS, Reverso) but lose those learning moments in browser history. The goal is to automate the collection of those searches and turn them into structured, revisable learning material — including AI-generated video overviews via NotebookLM.

**Key insight:** Google account sync means Chrome history on desktop includes searches from phone/tablet on the same Google account. UiPath targets `myactivity.google.com/product/search?hl=en` (Google Search activity only, clean list).

---

## 2. Solution Overview

UiPath-orchestrated pipeline:
1. UiPath scrapes Chrome/Google history → Excel
2. Python extracts German words → vocabulary files
3. UiPath uploads vocabulary to NotebookLM → AI video overview
4. Backup: Python crawls DWDS + generates PDF

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
| Primary output | NotebookLM video overview | Richer AI revision than static PDF; demonstrates modern RPA use case |
| Backup output | PDF via `fpdf2` | For demo/presentation purposes |
| Python trigger | `Start Process` with full Python path + Chr(34) quoting | Handles paths with spaces reliably |
| NotebookLM prompt textarea | `idx='3'` selector | Dynamic Angular Material IDs break strict selectors |
| Platform | Windows laptop | UiPath runs on Windows |

---

## 4. Pipeline

### Primary (NotebookLM Video)
```
[Chrome — myactivity.google.com/product/search?hl=en]
        |
        v
[UiPath: Extract Table Data → dtSearchHistory]
[UiPath: Write DataTable → raw_searches.xlsx]
        |
        v
[UiPath: Start Process → python 1_extract_words.py]
        |
        v
[Script 1: 1_extract_words.py]
  - Reads first column of raw_searches.xlsx
  - Filters "Searched for" entries only
  - Detects German by ä/ö/ü/ß or learning keywords
  - Deduplicates
  - Writes: output/notebooklm_source.txt  ← for NotebookLM
  - Writes: output/vocabulary_words.xlsx  ← for PDF backup
  - Writes: input/url_list.txt            ← for DWDS crawl
        |
        v
[UiPath: Go To URL → notebooklm.google.com]
[UiPath: Click New Notebook]
[UiPath: Upload notebooklm_source.txt]
[UiPath: Click Video Overview]
[UiPath: Type custom prompt]
[UiPath: Click Generate]
[UiPath: Message Box "Process completed"]
        |
        v
[NotebookLM generates AI video overview of German words]
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
RPA/  (repo root)
├── GermanDigest/
│   ├── input/
│   │   ├── raw_searches.xlsx         ← UiPath writes here (gitignored)
│   │   ├── url_list.txt              ← Script 1 writes here (gitignored)
│   │   └── sample_raw_searches.xlsx  ← test input (committed)
│   ├── output/
│   │   ├── notebooklm_source.txt     ← Script 1 writes — UiPath uploads this
│   │   ├── vocabulary_words.xlsx     ← Script 1 main output
│   │   ├── vocabulary_YYYYMMDD.xlsx  ← Script 3 enriched output
│   │   └── digest_YYYYMMDD.pdf       ← Script 4 output
│   ├── archive/
│   │   └── YYYYMMDD_crawl.tar.gz    ← Script 2 output
│   └── scripts/
│       ├── 1_extract_words.py        ← parses UiPath format + writes txt
│       ├── 2_tar_creator.py
│       ├── 3_extractor.py
│       └── 4_pdf_generator.py
├── UiPath/GermanDigestBot/
│   └── Main.xaml                     ← COMPLETE — full pipeline
├── PRODUCT_DOC.md                    ← this file
└── README.md                         ← Windows setup guide

GitHub: https://github.com/Gudakesh15/RPA
```

---

## 6. UiPath Workflow — Full State (Main.xaml)

**All inside one `Use Application/Browser` block (Chrome):**

| Step | Activity | Detail |
|------|----------|--------|
| 1 | Delay | 5s — page load |
| 2 | Extract Table Data | → dtSearchHistory (single text column) |
| 3 | Use Excel File + Write DataTable | → raw_searches.xlsx, sheet RawSearches |
| 4 | Start Process | python.exe + 1_extract_words.py |
| 5 | Delay | 30s — Script 1 runs |
| 6 | Go To URL | notebooklm.google.com |
| 7 | Click | New notebook (SPAN in welcome-page) |
| 8 | Delay | 5s |
| 9 | Click | Upload file (SPAN in add-sources-dialog) |
| 10 | Delay | 2s |
| 11 | Type Into | File path into Windows Open dialog |
| 12 | Click | Open button (Windows file picker) |
| 13 | Delay | 10s — upload processes |
| 14 | Click | Video Overview (chevron_forward MAT-ICON) |
| 15 | Delay | 4s |
| 16 | Mouse Scroll | Down in MAT-DIALOG-CONTENT |
| 17 | Delay | 5s |
| 18 | Click | TEXTAREA idx='3' (custom prompt box) |
| 19 | Type Into | Custom prompt text |
| 20 | Click | Generar/Generate (fuzzy selector, SPAN) |
| 21 | Delay | 5s |
| 22 | Message Box | "Process completed" |

---

## 7. File Index

| File | Purpose | Status |
|---|---|---|
| `GermanDigest/scripts/1_extract_words.py` | Parse UiPath output → filter German → write xlsx + txt | Done, filter needs improvement |
| `GermanDigest/scripts/2_tar_creator.py` | Crawl DWDS → TAR archive | Done |
| `GermanDigest/scripts/3_extractor.py` | Parse TAR → enriched vocabulary Excel | Done |
| `GermanDigest/scripts/4_pdf_generator.py` | Vocabulary Excel → PDF | Done |
| `GermanDigest/input/sample_raw_searches.xlsx` | Test input file | Done |
| `UiPath/GermanDigestBot/Main.xaml` | UiPath workflow — full pipeline | COMPLETE |
| `PRODUCT_DOC.md` | This file | Updated Session 2 |
| `README.md` | Windows setup guide | Done |

---

## 8. Python Dependencies

```
pip install requests beautifulsoup4 pandas openpyxl fpdf2
```

Run with: `C:\Python313\python.exe -m pip install ...`

---

## 9. Progress Tracker

| Task | Status |
|---|---|
| Project architecture defined | ✓ Done |
| GitHub repo set up | ✓ Done |
| Script 1: extract_words.py | ✓ Done (filter improvement pending) |
| Script 2: tar_creator.py | ✓ Done |
| Script 3: extractor.py | ✓ Done |
| Script 4: pdf_generator.py | ✓ Done |
| Sample test input created | ✓ Done |
| UiPath: open Chrome + navigate to myactivity | ✓ Done |
| UiPath: Extract Table Data → raw_searches.xlsx | ✓ Done |
| UiPath: Start Process → trigger Script 1 | ✓ Done |
| UiPath: Go To URL → notebooklm.google.com | ✓ Done |
| UiPath: Create new notebook | ✓ Done |
| UiPath: Upload notebooklm_source.txt | ✓ Done |
| UiPath: Trigger Video Overview | ✓ Done |
| UiPath: Enter custom prompt | ✓ Done |
| UiPath: Generate video | ✓ Done |
| UiPath: Message Box confirmation | ✓ Done |
| End-to-end test + recording | ✓ Done (Session 2) |
| Feedback session presentation | ✓ Done (29 May) |
| Script 1: improve German word filter | ⬜ To do (Session 3) |
| UiPath: data filtering loop (Excel → loop → build txt) | ⬜ To do (Session 3) |
| UiPath: DWDS enrichment loop | ⬜ To do (Session 3) |
| UiPath: conditional logic (skip if 0 words) | ⬜ To do (Session 3) |
| UiPath: run log to Excel | ⬜ To do (Session 3) |
| UiPath: name notebook with today's date | ⬜ To do (Session 3) |
| Final presentation (full demo) | ⬜ To do |
| Final report | ⬜ To do |

---

## 10. Next Session — Immediate Tasks (Session 3)

### Priority 1: Fix Script 1 German word filter
The filter currently misses real German words and includes false positives.

**What to investigate:**
- Print all "Searched for" entries from the test run to see what the script is seeing
- Check why German words with no umlauts (e.g. "gemütlich" without typing umlauts) are missed
- Exclude entries that: contain numbers, are longer than 4 words, contain domain names (.com, .de)
- Add a proper German word list or use langdetect library as a more reliable fallback

**Quick improvement to try:**
```python
# Exclude if entry has numbers (addresses like "Chausseestraße 12")
if re.search(r'\d', term):
    continue
# Exclude if clearly a URL fragment
if any(x in term.lower() for x in ['.com', '.de', '.org', 'http']):
    continue
```

### Priority 2: Move data processing into UiPath (better grades)
Currently Script 1 does all filtering AND builds the txt file. Move the txt-building step into UiPath:

**UiPath steps to add (after Start Process + Delay):**
1. `Use Excel File` → Read `vocabulary_words.xlsx` with `Read Range` → new DataTable variable (e.g. `dtVocab`)
2. `For Each Row in Data Table` → loop through `dtVocab`
   - `If` condition: `row("word").ToString.Trim.Length > 2`
   - If True: append word to a String variable (`vocabularyList`)
3. `Write Text File` → write `vocabularyList` to `notebooklm_source.txt`

This means UiPath is doing the data cleaning, not Python. Python only does the initial parse.

### Priority 3: Add conditional logic
```
If dtVocab.Rows.Count > 0
  Then: proceed to NotebookLM block
  Else: Message Box "No German words found this session. Bot finished."
```

### Priority 4: Name the notebook with today's date
After clicking "New notebook", UiPath should type a name:
- `Type Into` → notebook title field
- Text: `"German Vocab — " & DateTime.Now.ToString("dd MMM yyyy")`

### Priority 5: Run log
After the workflow completes, append a row to `run_log.xlsx`:
- Date, word count, notebook name, status (Success/Failed)

---

## 11. Future Vision (After Session 3)

| Feature | Description |
|---|---|
| Daily scheduling | Windows Task Scheduler or UiPath Orchestrator triggers bot each morning |
| Multi-source scraping | Also pull searches from DeepL, Duden, Linguee history tabs |
| LLM enrichment | Call OpenAI/Anthropic API to add definitions and example sentences before NotebookLM upload |
| Anki export | Generate Anki flashcard deck from vocabulary list |
| Multi-language | Extend filter to French, Spanish, Italian |
| Email digest | UiPath sends weekly summary email with word count + NotebookLM link |
| Orchestrator dashboard | Track vocabulary growth over time |

---

## 12. Presentation Outline (Feedback Session — 29 May)

See separate PRESENTATION.md for full slide-by-slide content.

**10-minute structure:**
1. Problem (1.5 min)
2. Solution overview (1.5 min)
3. Design approach — why UiPath + Python (2 min)
4. Pipeline walkthrough (2 min)
5. Live demo / results (2 min)
6. Next steps (1 min)

---

## 13. Team Work Division

| Person | Responsibility |
|---|---|
| Rodrigo | UiPath workflow — full pipeline build, NotebookLM automation |
| Avi | Python scripts — extraction, filtering, PDF, DWDS crawl |
| Person 3 | Testing, presentation, report |

---

*This document is updated continuously. Session 2 ended: 2026-05-23. MVP complete and recorded.*
