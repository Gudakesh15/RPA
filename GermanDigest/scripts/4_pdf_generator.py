# -*- coding: utf-8 -*-
"""
Step 4: Generate the PDF learning digest from the vocabulary Excel file.
Reads output/vocabulary_YYYYMMDD.xlsx, writes output/digest_YYYYMMDD.pdf.
Requires: pip install fpdf2 openpyxl
"""

import pandas as pd
import datetime
from pathlib import Path
from fpdf import FPDF

BASE_DIR   = Path(__file__).parent.parent  # GermanDigest/
OUTPUT_DIR = BASE_DIR / "output"

dn       = datetime.datetime.now()
IN_FILE  = OUTPUT_DIR / f"vocabulary_{dn.strftime('%Y%m%d')}.xlsx"
OUT_FILE = OUTPUT_DIR / f"digest_{dn.strftime('%Y%m%d')}.pdf"


class DigestPDF(FPDF):

    def header(self):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(80, 80, 80)
        self.cell(0, 8, 'German Vocabulary Digest', align='R')
        self.ln(12)

    def footer(self):
        self.set_y(-12)
        self.set_font('Helvetica', '', 8)
        self.set_text_color(150, 150, 150)
        self.cell(0, 8, f'Page {self.page_no()}', align='C')

    def title_page(self, date_str, word_count):
        self.add_page()
        self.set_font('Helvetica', 'B', 24)
        self.set_text_color(30, 30, 30)
        self.ln(40)
        self.cell(0, 12, 'German Vocabulary Digest', align='C')
        self.ln(14)
        self.set_font('Helvetica', '', 14)
        self.set_text_color(100, 100, 100)
        self.cell(0, 8, date_str, align='C')
        self.ln(10)
        self.cell(0, 8, f'{word_count} words collected', align='C')

    def summary_section(self, word_count):
        self.add_page()
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, 'Summary', ln=True)
        self.set_font('Helvetica', '', 11)
        self.set_text_color(60, 60, 60)
        self.multi_cell(0, 7, f'{word_count} unique German words were found in your browser history and processed into this digest.')
        self.ln(4)

    def word_card(self, index, row):
        self.ln(6)
        # word heading
        self.set_font('Helvetica', 'B', 13)
        self.set_text_color(20, 80, 160)
        self.cell(0, 9, f"{index}. {row['word']}", ln=True)

        def labeled_row(label, value):
            if not value or str(value).strip() in ('', 'nan'):
                return
            self.set_font('Helvetica', 'B', 10)
            self.set_text_color(80, 80, 80)
            self.cell(28, 6, label, ln=False)
            self.set_font('Helvetica', '', 10)
            self.set_text_color(30, 30, 30)
            self.multi_cell(0, 6, str(value).strip())

        labeled_row('Meaning:',    row.get('meaning', ''))
        labeled_row('Example:',    row.get('example', ''))
        labeled_row('Note:',       row.get('usage_note', ''))
        labeled_row('Source:',     row.get('source', ''))

        # separator line
        self.set_draw_color(200, 200, 200)
        self.line(self.get_x(), self.get_y() + 2, 200, self.get_y() + 2)


# --- main ---
df = pd.read_excel(str(IN_FILE))
date_str   = dn.strftime('%d %B %Y')
word_count = len(df)

pdf = DigestPDF()
pdf.set_auto_page_break(auto=True, margin=15)

pdf.title_page(date_str, word_count)
pdf.summary_section(word_count)

pdf.add_page()
pdf.set_font('Helvetica', 'B', 14)
pdf.set_text_color(30, 30, 30)
pdf.cell(0, 10, 'Vocabulary Cards', ln=True)

for i, row in df.iterrows():
    pdf.word_card(i + 1, row)

pdf.output(str(OUT_FILE))
print(f"PDF saved: {OUT_FILE}")
