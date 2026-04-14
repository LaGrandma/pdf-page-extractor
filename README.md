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
| `--end` | `150` | Last page to extract |

> **Note:** The extracted range is capped at 150 pages. If your `--start`/`--end` range spans more than 150 pages, it will be automatically clamped.

## Output

The script prints the total page count, the range being extracted, and the final file size so you can confirm it fits within any upload limits before sharing.

```
Total pages in source PDF: 612
Extracting pages 1–150 (150 pages)...
Saved: my_book_extracted.pdf  (18.3 MB)
```
