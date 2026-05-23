# -*- coding: utf-8 -*-
"""
Step 1: Extract German words from UiPath browser history output.
Reads input/raw_searches.xlsx (UiPath format: single column with
'Searched for [term]' entries), filters for German words,
deduplicates, builds DWDS URLs, writes input/url_list.txt.
"""

import pandas as pd
import re
from pathlib import Path

BASE_DIR      = Path(__file__).parent.parent  # GermanDigest/
INPUT_FILE    = BASE_DIR / "input" / "raw_searches.xlsx"
URL_LIST      = BASE_DIR / "input" / "url_list.txt"
VOCAB_OUT     = BASE_DIR / "output" / "vocabulary_words.xlsx"
NOTEBOOKLM_TXT = BASE_DIR / "output" / "notebooklm_source.txt"

# Words to strip from search queries
FILLER = {
    'meaning', 'translation', 'bedeutung', 'deutsch', 'english',
    'example', 'übersetzung', 'synonym', 'definition', 'german',
    'reverso', 'linguee', 'duden', 'dwds', 'was', 'bedeutet',
    'auf', 'in', 'the', 'a', 'an'
}

# German indicators: umlauts, ß, or known learning keywords
GERMAN_CHARS = set('äöüÄÖÜß')
GERMAN_KEYWORDS = {
    'bedeutung', 'übersetzung', 'auf deutsch', 'was bedeutet',
    'duden', 'dwds', 'meaning', 'translation', 'deutsch', 'german'
}


def is_german_related(term):
    term_lower = term.lower()
    # Contains German characters
    if any(c in GERMAN_CHARS for c in term):
        return True
    # Contains German learning keywords
    if any(kw in term_lower for kw in GERMAN_KEYWORDS):
        return True
    return False


def extract_search_term(raw_text):
    raw_text = str(raw_text).strip()
    # Only process "Searched for" entries
    if not raw_text.startswith('Searched for '):
        return None
    # Extract term: between "Searched for " and first \n or end
    term = raw_text.replace('Searched for ', '', 1)
    term = term.split('\\n')[0].split('\n')[0].strip()
    # Remove trailing metadata like "• Details"
    term = re.sub(r'\s*•.*$', '', term).strip()
    return term if term else None


def clean_term(term):
    tokens = re.split(r'\s+', term.lower())
    tokens = [t for t in tokens if t and t not in FILLER]
    return ' '.join(tokens) if tokens else None


def build_dwds_url(word):
    return f"https://www.dwds.de/wb/{word.split()[0]}"


# Read the UiPath output — single column, any name
df = pd.read_excel(INPUT_FILE, header=0)
raw_column = df.iloc[:, 0]  # always use first column regardless of name

seen  = set()
rows  = []

for raw in raw_column.dropna():
    term = extract_search_term(raw)
    if not term:
        continue
    if not is_german_related(term):
        continue
    cleaned = clean_term(term)
    if not cleaned or cleaned in seen:
        continue
    seen.add(cleaned)
    rows.append({
        'id':       len(rows) + 1,
        'word':     term,
        'cleaned':  cleaned,
        'dwds_url': build_dwds_url(cleaned)
    })

# Write url_list.txt for the TAR creator
with open(URL_LIST, 'w', encoding='utf-8') as f:
    for r in rows:
        f.write(f"{r['id']}\t{r['dwds_url']}\t{r['cleaned']}\n")

# Write vocabulary Excel for PDF backup
(BASE_DIR / "output").mkdir(parents=True, exist_ok=True)
pd.DataFrame(rows)[['id', 'word', 'cleaned', 'dwds_url']].to_excel(
    str(VOCAB_OUT), index=False, sheet_name='Vocabulary'
)

# Write plain-text source for NotebookLM upload
import datetime
today = datetime.date.today().strftime('%d %B %Y')
with open(NOTEBOOKLM_TXT, 'w', encoding='utf-8') as f:
    f.write(f"German Vocabulary — {today}\n")
    f.write("=" * 40 + "\n\n")
    f.write("Words searched this period:\n\n")
    for r in rows:
        f.write(f"- {r['word']}\n")
    f.write("\n")
    f.write("Source: Google search history (myactivity.google.com)\n")

print(f"Done. {len(rows)} German words found.")
print(f"  url_list       -> {URL_LIST}")
print(f"  vocabulary     -> {VOCAB_OUT}")
print(f"  notebooklm_src -> {NOTEBOOKLM_TXT}")
