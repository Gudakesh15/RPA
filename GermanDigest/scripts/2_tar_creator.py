# -*- coding: utf-8 -*-
"""
Step 2: Crawl DWDS pages for each word and archive the HTML.
Adapted from Avi's Crawler / 1_TarFileCreator.py.
Reads input\url_list.txt, crawls each DWDS URL, saves HTML to archive\crawl_YYYYMMDD.tar.gz.
"""

import requests
import csv
import os
import tarfile
import datetime
from pathlib import Path

BASE_DIR    = Path(r"C:\GermanDigest")
URL_LIST    = BASE_DIR / "input" / "url_list.txt"
ARCHIVE_DIR = BASE_DIR / "archive"

dn       = datetime.datetime.now()
TAR_OUT  = ARCHIVE_DIR / f"{dn.strftime('%Y%m%d')}_crawl.tar.gz"

TEST_MODE  = 0
SIZE_LIMIT = 500   # DWDS pages are small; flag anything under 500 chars as blocked

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
]


def set_user_agent(session, pick):
    session.headers.update({'user-agent': USER_AGENTS[pick % len(USER_AGENTS)]})


def crawl_url(session, url):
    attempts = 0
    while attempts < 5:
        try:
            resp = session.get(url, timeout=15)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            attempts += 1
            print(f"  Retry {attempts}: {e}")
    return ''


def write_to_tar(tar_handle, tmp_path, word_id, html):
    tmp_file = tmp_path / f"{word_id}.html"
    tmp_file.write_text(html, encoding='utf-8')
    tar_handle.add(str(tmp_file), arcname=f"{word_id}.html")
    tmp_file.unlink()


# --- read URL list ---
urls = []
with open(URL_LIST, 'r', encoding='utf-8') as f:
    for row in csv.reader(f, delimiter='\t'):
        if len(row) >= 3:
            urls.append({'id': row[0], 'url': row[1], 'word': row[2]})

crawl_limit = 10 if TEST_MODE else len(urls)

s = requests.Session()
s.headers.update({'accept-language': 'de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7'})
set_user_agent(s, 0)

tmp_path = BASE_DIR / "archive" / "tmp"
tmp_path.mkdir(parents=True, exist_ok=True)

blocked = []

with tarfile.open(str(TAR_OUT), 'w:gz') as tar:
    for i, entry in enumerate(urls[:crawl_limit]):
        print(f"[{i+1}/{crawl_limit}] Crawling: {entry['word']} — {entry['url']}")
        set_user_agent(s, i)
        html = crawl_url(s, entry['url'])

        if len(html) < SIZE_LIMIT:
            print(f"  Possibly blocked ({len(html)} chars). Retrying with different agent...")
            set_user_agent(s, i + 1)
            html = crawl_url(s, entry['url'])

        if len(html) < SIZE_LIMIT:
            print(f"  Blocked again — skipping.")
            blocked.append(entry['word'])
            continue

        if TEST_MODE != 1:
            write_to_tar(tar, tmp_path, entry['id'] + '_' + entry['word'], html)
        print(f"  OK ({len(html)} chars)")

tmp_path.rmdir()

print(f"\nArchive saved: {TAR_OUT}")
print(f"Blocked / skipped: {blocked if blocked else 'none'}")
