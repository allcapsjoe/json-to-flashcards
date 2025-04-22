#!/usr/bin/env python3
import argparse
import json
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.colors import black, white, limegreen
from reportlab.pdfbase import pdfmetrics

def wrap_text(text, font_name, font_size, max_width):
    """
    Splits `text` into lines that fit within `max_width` when rendered
    in the given font.
    """
    words = text.split()
    lines = []
    current = ""
    for word in words:
        test = f"{current} {word}".strip()
        if pdfmetrics.stringWidth(test, font_name, font_size) <= max_width:
            current = test
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines

def create_flashcards(json_path: str, pdf_path: str):
    # Load JSON
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    flashcards = data.get("flashcards", {})

    # Page dimensions: 9in × 16in
    PAGE_WIDTH, PAGE_HEIGHT = 9 * inch, 16 * inch
    MARGIN = 0.5 * inch
    TEXT_WIDTH = PAGE_WIDTH - 2 * MARGIN

    # Canvas setup
    c = canvas.Canvas(pdf_path, pagesize=(PAGE_WIDTH, PAGE_HEIGHT))

    # ─── FONT & LAYOUT SETTINGS ───────────────────────────────────────────────────
    QUESTION_FONT = "Helvetica-Bold"
    ANSWER_FONT   = "Helvetica"
    FOOTER_FONT   = "Helvetica-Oblique"

    QUESTION_SIZE = 72  # ←– Question font size
    ANSWER_SIZE   = 72  # ←– Answer font size
    FOOTER_SIZE   = 28  # ←– Footer font size

    # Adjust this value to increase/decrease the vertical gap
    # between the separator line and the footer text:
    FOOTER_SPACING = 0.5 * inch  # ←– spacing from line up to footer text
    # ───────────────────────────────────────────────────────────────────────────────

    counter = 1

    for section_title, cards in flashcards.items():
        for card in cards:
            # ——— Question page ———
            c.setFillColor(black)
            c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)

            c.setFillColor(white)
            c.setFont(QUESTION_FONT, QUESTION_SIZE)
            q_text = f"{counter}. {card['question']}"
            lines = wrap_text(q_text, QUESTION_FONT, QUESTION_SIZE, TEXT_WIDTH)
            y = PAGE_HEIGHT - MARGIN - QUESTION_SIZE
            for line in lines:
                c.drawString(MARGIN, y, line)
                y -= QUESTION_SIZE * 1.2

            # footer line & text
            c.setStrokeColor(white)
            c.setLineWidth(1)
            c.line(MARGIN, MARGIN, PAGE_WIDTH - MARGIN, MARGIN)
            footer_y = MARGIN + FOOTER_SPACING
            c.setFont(FOOTER_FONT, FOOTER_SIZE)
            c.drawCentredString(PAGE_WIDTH / 2, footer_y, section_title)

            c.showPage()

            # ——— Answer page ———
            c.setFillColor(black)
            c.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)

            c.setFillColor(limegreen)
            c.setFont(ANSWER_FONT, ANSWER_SIZE)
            a_text = card['answer']
            lines = wrap_text(a_text, ANSWER_FONT, ANSWER_SIZE, TEXT_WIDTH)
            y = PAGE_HEIGHT - MARGIN - ANSWER_SIZE
            for line in lines:
                c.drawString(MARGIN, y, line)
                y -= ANSWER_SIZE * 1.2

            # footer line & text
            c.setStrokeColor(white)
            c.setLineWidth(1)
            c.line(MARGIN, MARGIN, PAGE_WIDTH - MARGIN, MARGIN)
            footer_y = MARGIN + FOOTER_SPACING
            c.setFont(FOOTER_FONT, FOOTER_SIZE)
            c.drawCentredString(PAGE_WIDTH / 2, footer_y, section_title)

            c.showPage()
            counter += 1

    c.save()

def main():
    parser = argparse.ArgumentParser(
        description="Generate a 9×16 PDF flashcard deck from a JSON file"
    )
    parser.add_argument("json_file", help="Input JSON file path")
    parser.add_argument("pdf_file",  help="Output PDF file path")
    args = parser.parse_args()

    create_flashcards(args.json_file, args.pdf_file)

if __name__ == "__main__":
    main()
