# Feedback Session — Presentation Guide
## German Browser-to-NotebookLM Learning Digest Bot
**Date:** Friday 29 May 2026 | **Duration:** 10 minutes

---

## Slide 1 — Title

**Title:** German Vocabulary Bot
**Subtitle:** Automating language learning with UiPath + Python + NotebookLM
**Course:** RPA Seminar — Masters Semester 2
**Team:** Rodrigo · Avi · [Person 3]

---

## Slide 2 — The Problem (1.5 min)

**Title:** The Problem: Lost Vocabulary

**Bullets:**
- German learners search 5–20 words per day on Google, Duden, DeepL, DWDS
- Those searches disappear into browser history — never reviewed again
- Manual flashcard creation is time-consuming and never happens
- Learning moments are lost within hours

**Visual idea:** Screenshot of a long Google search history with German words scattered among unrelated searches — highlight how easy it is to lose them.

**What to say:**
> "Every German learner does this — you encounter an unknown word, you Google it, you understand it in the moment, and then it's gone. We wanted to automate the rescue of those words before they disappear."

---

## Slide 3 — The Solution (1.5 min)

**Title:** Our Solution: A Fully Automated Pipeline

**Bullets:**
- UiPath scrapes your Google search history automatically
- Python filters out only the German vocabulary words
- UiPath uploads them directly to NotebookLM
- NotebookLM generates an AI video — a personalised revision episode

**Visual idea:** Simple left-to-right flow diagram:
```
[Browser History] → [UiPath] → [Python] → [NotebookLM] → [AI Video]
```

**What to say:**
> "One click — or eventually, a daily scheduled run — and you get a personalised video of every German word you searched that day, explained and put in context by AI."

---

## Slide 4 — Design Approach: Why These Tools? (2 min)

**Title:** Design Decisions

**Table or bullet pairs:**

| Choice | Reason |
|---|---|
| `myactivity.google.com` instead of local Chrome history | Google syncs history across phone + laptop — one scrape gets everything |
| UiPath `Extract Table Data` | Captures the full search activity page as structured data |
| Python for word filtering | Regex + German character detection is code-level logic, better in Python than UiPath |
| NotebookLM over PDF | AI understands German context, generates richer audio + video revision |
| One UiPath browser session | Navigate from Google → NotebookLM in same Chrome window — no second login needed |

**What to say:**
> "The most important decision was using Google My Activity instead of the browser's local history. It means the bot picks up German words searched on your phone during the day — not just on the laptop where UiPath is running. That cross-device sync was the key insight."

---

## Slide 5 — Pipeline Walkthrough (2 min)

**Title:** How It Works — Step by Step

**Visual: numbered flow with icons (browser, spreadsheet, python logo, notebooklm)**

```
Step 1  UiPath opens myactivity.google.com
        → Extract Table Data (22 activities in one workflow)
        → Writes raw_searches.xlsx

Step 2  UiPath triggers Python via Start Process
        → Script reads Excel, finds "Searched for [word]" entries
        → Detects German: ä ö ü ß or learning keywords
        → Writes notebooklm_source.txt

Step 3  UiPath navigates to notebooklm.google.com
        → Creates new notebook
        → Uploads notebooklm_source.txt

Step 4  UiPath clicks Video Overview
        → Types custom prompt:
           "Create a short engaging video script that teaches these
            German vocabulary words through a creative storyline..."
        → Clicks Generate

Step 5  NotebookLM generates AI video
        UiPath shows: "Process completed"
```

**What to say:**
> "The entire flow is 22 UiPath activities inside a single browser automation block. The handoff between UiPath and Python happens through a file — Python reads the Excel UiPath wrote, and UiPath uploads the text file Python wrote. No API needed."

---

## Slide 6 — Demo / First Results (2 min)

**Title:** First Results

**Content:**

Show the recording of the full workflow running. While it plays, narrate:

> "You can see UiPath opening Google My Activity, scrolling through the search history, extracting it to Excel. Then it triggers the Python script. Then it opens NotebookLM — creates a new notebook — uploads the vocabulary file — navigates to the Video Overview panel — types the custom prompt — and clicks Generate."

**After the recording, show:**
- Screenshot of the NotebookLM notebook with the source file uploaded
- Screenshot of the video overview being generated
- The notebooklm_source.txt file content (show what gets uploaded — a clean list of German words)

**Metrics from first test:**
- Workflow runs in under 2 minutes (excluding the 30s Python delay)
- Successfully detects German words with umlauts (ä, ö, ü, ß)
- NotebookLM video generated successfully
- PDF backup also generated as alternative output

---

## Slide 7 — Technical Architecture (optional, if time allows)

**Title:** Under the Hood

**Two-path architecture diagram:**

```
PRIMARY PATH                    BACKUP PATH
─────────────────────           ──────────────────────
myactivity.google.com           vocabulary_words.xlsx
       ↓                               ↓
Extract Table Data              Script 2: DWDS crawl
       ↓                               ↓
raw_searches.xlsx               Script 3: HTML parse
       ↓                               ↓
Script 1: filter                Script 4: PDF generate
       ↓                               ↓
notebooklm_source.txt           digest_YYYYMMDD.pdf
       ↓
NotebookLM video
```

**UiPath activities used:**
- Use Application/Browser, Extract Table Data, Use Excel File
- Write DataTable, Start Process, Go To URL
- Click (×4), Type Into (×2), Mouse Scroll, Delay (×7), Message Box

---

## Slide 8 — What's Next (1 min)

**Title:** Next Steps

**Three clear improvements:**

**1. Smarter filtering (Python)**
- Exclude numbers/addresses (Chausseestraße 12)
- Use `langdetect` library for more accurate German detection
- Catch words without umlauts but clearly German (e.g. "gemütlich" typed without special chars)

**2. More UiPath involvement (for richer automation)**
- UiPath reads vocabulary Excel → loops through rows → builds the source file itself
- UiPath looks up each word on DWDS → extracts definition → writes back to Excel
- Conditional logic: if 0 German words found, skip NotebookLM and show a notification

**3. Scheduling**
- Windows Task Scheduler runs the bot every morning automatically
- Daily video digest ready before the first lesson

**What to say:**
> "The MVP proves the concept works. The next phase is making the filtering smarter and moving more data processing into UiPath itself — so the bot is truly autonomous, not just a trigger for Python."

---

## Slide 9 — Future Vision

**Title:** Where This Can Go

**Bullets:**
- **Multi-device:** Already works — Google sync includes phone searches
- **Multi-language:** Same architecture extends to French, Spanish, Italian
- **Richer content:** Call an LLM API to add definitions + example sentences before NotebookLM upload
- **Anki export:** Generate flashcard deck from vocabulary list
- **Email digest:** Weekly summary email with word count + NotebookLM notebook link
- **Scheduling:** Fully autonomous daily run via UiPath Orchestrator

**What to say:**
> "The architecture is modular — swapping out the German filter for French would take one line of code. And because UiPath is orchestrating everything, adding email notifications or a scheduling layer is straightforward."

---

## Slide 10 — Summary

**Title:** What We Built

**Three-line summary:**
1. **Process:** Fully automated German vocabulary rescue from browser history
2. **Tech:** UiPath (22 activities) + Python (4 scripts) + NotebookLM AI
3. **Result:** One run → personalised AI video revision of the day's German words

**Final line to say:**
> "This is RPA as it should be — taking a repetitive human task that nobody ever actually does, and making it happen automatically, every day, with a better output than the human would have produced."

---

## Timing Guide

| Slide | Time |
|-------|------|
| 1 — Title | 20s |
| 2 — Problem | 1:30 |
| 3 — Solution | 1:00 |
| 4 — Design decisions | 1:30 |
| 5 — Pipeline walkthrough | 1:30 |
| 6 — Demo + results | 2:00 |
| 7 — Architecture (optional) | skip if tight |
| 8 — Next steps | 1:00 |
| 9 — Future vision | 30s |
| 10 — Summary | 30s |
| **Total** | **~10 min** |

---

## Questions You Might Get — Prepared Answers

**Q: Why not just use a Chrome extension?**
> A Chrome extension can't trigger Python scripts, write to Excel, or automate NotebookLM. UiPath orchestrates the full cross-application pipeline — that's the value of RPA over a simple browser plugin.

**Q: Does this work if you search in German but in English? (e.g. "zuständig meaning")**
> Yes — Script 1 detects German keywords like "meaning" and "translation" as signals that the search was for a German word, even if the term itself has no umlauts.

**Q: What if NotebookLM's interface changes?**
> UiPath selectors would need to be re-indicated. We've already handled one case of this — the dynamic textarea IDs — by switching to positional selectors (`idx='3'`) instead of Angular Material IDs that change each page load.

**Q: Could this run daily automatically?**
> Yes — Windows Task Scheduler can trigger the UiPath workflow each morning. That's in the next session's plan.

**Q: How many words did you find in your test?**
> In our first live test, 1 of 6 German words was correctly identified. The filter is the main remaining work — the architecture and automation are proven, now we tune the detection.
