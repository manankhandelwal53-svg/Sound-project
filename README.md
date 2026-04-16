# CBSE Result Analyzer

CBSE Result Analyzer is a production-oriented Python application for extracting Class 10 result data from unstructured files and grouping students by user-defined benchmark ranges.

It supports:

- Digital PDFs through text extraction
- Scanned PDFs and images through OCR
- DOCX files through document parsing
- Plain text files for quick validation and testing
- CLI and Streamlit interfaces
- CSV and Excel export
- Logging and uncertainty flags for manual review

## Features

- Extracts `student name`, `subject code`, and `marks`
- Handles multi-line and inconsistent layouts such as:

```text
Manan        087
             90
```

- Validates marks in the `0-100` range
- Prevents duplicate records with source-aware deduplication
- Flags uncertain OCR or parse results instead of silently guessing
- Filters results against ranges like `33-44.5`, `45-60`, or `90-100`
- Scales to large result files by processing pages sequentially and parsing line-by-line

## Project Structure

```text
src/cbse_result_analyzer/
  cli.py
  streamlit_app.py
  config.py
  exporters.py
  logging_config.py
  models.py
  extraction/
  parsing/
  services/
tests/
samples/
```

## Installation

1. Install Python 3.10+
2. Install Tesseract OCR and ensure it is available on PATH
3. Install the package:

```bash
pip install -e .[dev]
```

If Tesseract is installed outside `PATH`, set `TESSERACT_CMD` to the full executable path before running the app.

PowerShell example:

```powershell
$env:TESSERACT_CMD="D:\teseract\tesseract.exe"
```

## CLI Usage

```bash
cbse-result-analyzer analyze ^
  --input samples\sample_results.txt ^
  --range 33-44.5 ^
  --export-csv output\benchmark.csv ^
  --export-xlsx output\benchmark.xlsx
```

You can also override the OCR binary path explicitly:

```bash
cbse-result-analyzer analyze --input samples\sample_results.txt --range 33-44.5 --tesseract-cmd D:\teseract\tesseract.exe
```

### Commands

- `analyze`: extracts records, applies a benchmark range, and prints results

### Example Output

```text
Range: 33.0-44.5
Students:
- Rahul - 40
- Priya - 35

Total: 2 students
Uncertain records: 1
```

## Streamlit UI

```bash
streamlit run src/cbse_result_analyzer/streamlit_app.py
```

The UI provides:

- File upload
- Benchmark range input
- Results table
- Export to CSV and Excel
- Warnings for uncertain records

## Accuracy Strategy

The pipeline prioritizes accuracy over speed:

- Digital text extraction is attempted before OCR
- OCR text is preprocessed with OpenCV
- Parsing uses deterministic rules with confidence scoring
- Records outside valid mark range are rejected
- Ambiguous rows are retained as flagged items for review

## Testing

Run:

```bash
pytest
```

Included tests cover:

- Clean text extraction patterns
- Messy multi-line layouts
- Duplicate handling
- Benchmark filtering
- Validation and uncertainty behavior

## Notes

- OCR quality depends on scan quality and Tesseract language configuration
- For best results on scanned PDFs, use grayscale or clean monochrome scans
- A local Python interpreter was not available in the current build environment, so you should run the verification steps after installing Python and dependencies
