# -*- coding: utf-8 -*-
"""
Step 3: Parse archived DWDS HTML pages and extract vocabulary data.
Adapted from Avi's Crawler / 2_Dormeo Information extractor.py.
Reads archive/crawl_YYYYMMDD.tar.gz, writes output/vocabulary_YYYYMMDD.xlsx.
"""

import os
import tarfile
import datetime
import re
import pandas as pd
from pathlib import Path
from bs4 import BeautifulSoup

BASE_DIR    = Path(__file__).parent.parent  # GermanDigest/
ARCHIVE_DIR = BASE_DIR / "archive"
OUTPUT_DIR  = BASE_DIR / "output"

dn       = datetime.datetime.now()
TAR_IN   = ARCHIVE_DIR / f"{dn.strftime('%Y%m%d')}_crawl.tar.gz"
OUT_FILE = OUTPUT_DIR / f"vocabulary_{dn.strftime('%Y%m%d')}.xlsx"

TEST_MODE = 0


def parse_dwds_page(html, word):
    soup = BeautifulSoup(html, 'html.parser')
    entry = {'word': word, 'meaning': '', 'example': '', 'usage_note': '', 'source': f"https://www.dwds.de/wb/{word}"}

    # definition — lives on a <span>, not a <div>
    definition_tag = soup.find(class_='dwdswb-definition')
    if definition_tag:
        entry['meaning'] = definition_tag.get_text(separator=' ', strip=True)[:300]

    # best example sentence: kompetenzbeispiel first, belegtext as fallback
    example_tag = soup.find(class_='dwdswb-kompetenzbeispiel') or soup.find(class_='dwdswb-belegtext')
    if example_tag:
        entry['example'] = example_tag.get_text(separator=' ', strip=True)[:300]

    return entry


print(f"Opening archive: {TAR_IN}")
tf = tarfile.open(str(TAR_IN))
file_list = tf.getmembers()
print(f"Found {len(file_list)} files in archive.")

records = []
count   = 0

for f in file_list:
    count += 1
    if TEST_MODE and count > 10:
        break

    word = f.name.replace('.html', '').split('_', 1)[-1]  # strip leading ID

    extracted = tf.extractfile(f)
    if extracted is None:
        continue
    html = extracted.read().decode('utf-8', errors='replace')

    record = parse_dwds_page(html, word)
    records.append(record)

    if count % 10 == 0:
        print(f"  Parsed {count} files...")

tf.close()

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df = pd.DataFrame(records, columns=['word', 'meaning', 'example', 'usage_note', 'source'])
df.to_excel(str(OUT_FILE), index=False, sheet_name='Vocabulary')

print(f"\nDone. {len(records)} words written to {OUT_FILE}")
