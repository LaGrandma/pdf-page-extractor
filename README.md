# PDF Page Extractor

Extract up to 150 pages from a large PDF into a new, smaller file — useful for working around upload size limits.

## Requirements

- Python 3.7+

> `pypdf` is installed automatically the first time you run the script.

## Usage

```bash
python3 extract_pdf_pages.py <input.pdf> [output.pdf] [--start N] [--end N]
```

### Examples

**Extract the first 150 pages (default):**
```bash
python3 extract_pdf_pages.py my_book.pdf
```

**Extract a specific range:**
```bash
python3 extract_pdf_pages.py my_book.pdf output.pdf --start 80 --end 229
```

**Custom output filename:**
```bash
python3 extract_pdf_pages.py my_book.pdf chapter1.pdf --start 1 --end 150
```

## Options

| Option | Default | Description |
|--------|---------|-------------|
| `input` | *(required)* | Path to the source PDF |
| `output` | `input_extracted.pdf` | Path for the output PDF |
| `--start` | `1` | First page to extract (1-indexed) |
| `--end` | *(start + limit - 1)* | Last page to extract |
| `--limit` | `150` | Max pages to extract (up to 300) |

## Chapter-aware extraction

If the PDF has a table of contents, the script automatically snaps to the nearest chapter boundary before the limit — so you never cut off mid-chapter.

For example, with `--limit 150`, if a chapter ends at page 137 and the next one would go past 150, the script stops at 137.

If the PDF has no bookmarks, it falls back to the exact page limit.

## Output

```
Total pages in source PDF: 612
Snapping to nearest chapter boundary: page 137 (chapter ends here before limit of 150)
Extracting pages 1–137 (137 pages)...
Saved: my_book_extracted.pdf  (15.2 MB)
```
