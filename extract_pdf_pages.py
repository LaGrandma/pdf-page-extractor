#!/usr/bin/env python3
"""
Extract up to 150 pages from a PDF file into a new PDF.
Usage: python3 extract_pdf_pages.py input.pdf [output.pdf] [--start N] [--end N]
"""

import sys
import argparse
from pathlib import Path


def extract_pages(input_path: str, output_path: str, start: int, end: int):
    try:
        from pypdf import PdfReader, PdfWriter
    except ImportError:
        try:
            from PyPDF2 import PdfReader, PdfWriter
        except ImportError:
            print("Error: Install pypdf first:  pip install pypdf")
            sys.exit(1)

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    print(f"Total pages in source PDF: {total_pages}")

    # Clamp range to valid bounds
    start = max(1, start)
    end = min(end, total_pages)

    # Enforce 150-page maximum
    if end - start + 1 > 150:
        end = start + 149
        print(f"Range clamped to 150 pages: {start}–{end}")

    print(f"Extracting pages {start}–{end} ({end - start + 1} pages)...")

    writer = PdfWriter()
    for i in range(start - 1, end):  # PdfReader is 0-indexed
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    size_mb = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"Saved: {output_path}  ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Extract up to 150 pages from a PDF.")
    parser.add_argument("input", help="Path to the source PDF")
    parser.add_argument("output", nargs="?", help="Output PDF path (default: input_extracted.pdf)")
    parser.add_argument("--start", type=int, default=1, help="First page to extract (1-indexed, default: 1)")
    parser.add_argument("--end", type=int, default=150, help="Last page to extract (default: 150)")
    args = parser.parse_args()

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    output_path = args.output or str(input_path.stem) + "_extracted.pdf"
    extract_pages(str(input_path), output_path, args.start, args.end)


if __name__ == "__main__":
    main()
