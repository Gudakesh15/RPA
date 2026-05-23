# -*- coding: utf-8 -*-
"""
Step 1: Extract German words from raw URLs written by UiPath.
Reads input\raw_searches.xlsx, strips filler words, deduplicates,
builds DWDS lookup URLs, writes input\url_list.txt for the TAR creator.
"""

import pandas as pd
import re
import os
from urllib.parse import urlparse, parse_qs, unquote
from pathlib import Path

BASE_DIR = Path(r"C:\GermanDigest")
INPUT_FILE  = BASE_DIR / "input" / "raw_searches.xlsx"
URL_LIST    = BASE_DIR / "input" / "url_list.txt"

FILLER = {
    'meaning', 'translation', 'bedeutung', 'deutsch', 'english',
    'example', 'übersetzung', 'synonym', 'was', 'bedeutet', 'auf',
    'definition', 'german', 'auf deutsch', 'in english', 'reverso',
    'linguee', 'duden', 'dwds'
}


def extract_word(url):
    url = str(url).strip()
    parsed = urlparse(url)

    if 'google' in parsed.netloc:
        q = parse_qs(parsed.query).get('q', [''])[0]
        tokens = re.split(r'[\s+]+', unquote(q).lower())
        tokens = [t for t in tokens if t and t not in FILLER]
        return tokens[0] if tokens else None

    if 'duden' in parsed.netloc or 'dwds' in parsed.netloc:
        return unquote(parsed.path.split('/')[-1]) or None

    if 'deepl' in parsed.netloc:
        # fragment: de/en/beantragen
        parts = parsed.fragment.split('/')
        return parts[-1] if parts else None

    if 'linguee' in parsed.netloc or 'reverso' in parsed.netloc:
        q = parse_qs(parsed.query).get('query', [''])[0] or \
            parse_qs(parsed.query).get('q', [''])[0]
        tokens = re.split(r'[\s+]+', unquote(q).lower())
        tokens = [t for t in tokens if t and t not in FILLER]
        return tokens[0] if tokens else None

    return None


def build_dwds_url(word):
    return f"https://www.dwds.de/wb/{word}"


df = pd.read_excel(INPUT_FILE)

seen  = set()
rows  = []
for url in df['url'].dropna():
    word = extract_word(url)
    if word and word not in seen:
        seen.add(word)
        rows.append({'id': len(rows) + 1, 'word': word, 'dwds_url': build_dwds_url(word)})

with open(URL_LIST, 'w', encoding='utf-8') as f:
    for r in rows:
        f.write(f"{r['id']}\t{r['dwds_url']}\t{r['word']}\n")

print(f"Done. {len(rows)} unique words written to {URL_LIST}")
