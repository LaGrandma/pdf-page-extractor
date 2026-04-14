#!/usr/bin/env python3
"""
Extract up to N pages from a PDF file into a new PDF.
Optionally snaps to the nearest chapter boundary before the limit.
Usage: python3 extract_pdf_pages.py input.pdf [output.pdf] [--start N] [--end N] [--limit N]
"""

import sys
import argparse
from pathlib import Path

MAX_PAGE_LIMIT = 300


def ensure_pypdf():
    try:
        import pypdf  # noqa: F401
    except ImportError:
        print("pypdf not found, installing...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pypdf"])
        print("pypdf installed successfully.\n")


def get_chapter_end_pages(reader):
    """Return a sorted list of page numbers (1-indexed) where chapters end."""
    try:
        outline = reader.outline
    except Exception:
        return []

    chapter_starts = []

    def collect_starts(items):
        for item in items:
            if isinstance(item, list):
                collect_starts(item)
            else:
                try:
                    page_num = reader.get_destination_page_number(item) + 1  # 1-indexed
                    chapter_starts.append(page_num)
                except Exception:
                    pass

    collect_starts(outline)

    if not chapter_starts:
        return []

    chapter_starts = sorted(set(chapter_starts))
    total = len(reader.pages)

    # Chapter ends are the page before the next chapter starts
    chapter_ends = [chapter_starts[i + 1] - 1 for i in range(len(chapter_starts) - 1)]
    chapter_ends.append(total)

    return chapter_ends


def snap_to_chapter(end_page, chapter_ends):
    """Return the last chapter-end page that is <= end_page."""
    candidates = [p for p in chapter_ends if p <= end_page]
    if not candidates:
        return end_page  # No chapter boundary found, use original limit
    snapped = max(candidates)
    if snapped != end_page:
        print(f"Snapping to nearest chapter boundary: page {snapped} (chapter ends here before limit of {end_page})")
    return snapped


def extract_pages(input_path: str, output_path: str, start: int, end: int, limit: int):
    ensure_pypdf()
    from pypdf import PdfReader, PdfWriter

    reader = PdfReader(input_path)
    total_pages = len(reader.pages)
    print(f"Total pages in source PDF: {total_pages}")

    # Clamp range to valid bounds
    start = max(1, start)
    end = min(end, total_pages)

    # Enforce page limit
    if end - start + 1 > limit:
        end = start + limit - 1
        print(f"Range exceeds limit, capping at {limit} pages (page {end})")

    # Try to snap to nearest chapter boundary
    chapter_ends = get_chapter_end_pages(reader)
    if chapter_ends:
        end = snap_to_chapter(end, chapter_ends)
    else:
        print("No chapter bookmarks found in this PDF — using exact page limit.")

    print(f"Extracting pages {start}–{end} ({end - start + 1} pages)...")

    writer = PdfWriter()
    for i in range(start - 1, end):  # PdfReader is 0-indexed
        writer.add_page(reader.pages[i])

    with open(output_path, "wb") as f:
        writer.write(f)

    size_mb = Path(output_path).stat().st_size / (1024 * 1024)
    print(f"Saved: {output_path}  ({size_mb:.1f} MB)")


def main():
    parser = argparse.ArgumentParser(description="Extract pages from a PDF, snapping to chapter boundaries.")
    parser.add_argument("input", help="Path to the source PDF")
    parser.add_argument("output", nargs="?", help="Output PDF path (default: input_extracted.pdf)")
    parser.add_argument("--start", type=int, default=1, help="First page to extract (1-indexed, default: 1)")
    parser.add_argument("--end", type=int, default=None, help="Last page to extract (default: start + limit - 1)")
    parser.add_argument("--limit", type=int, default=150,
                        help=f"Max number of pages to extract (default: 150, max: {MAX_PAGE_LIMIT})")
    args = parser.parse_args()

    if args.limit > MAX_PAGE_LIMIT:
        print(f"Error: --limit cannot exceed {MAX_PAGE_LIMIT}.")
        sys.exit(1)
    if args.limit < 1:
        print("Error: --limit must be at least 1.")
        sys.exit(1)

    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {input_path}")
        sys.exit(1)

    end = args.end if args.end is not None else args.start + args.limit - 1
    output_path = args.output or str(input_path.stem) + "_extracted.pdf"
    extract_pages(str(input_path), output_path, args.start, end, args.limit)


if __name__ == "__main__":
    main()
