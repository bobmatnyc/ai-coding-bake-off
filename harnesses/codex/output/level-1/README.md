# Markdown Table Formatter

Level 1 solution for the AI coding bake-off.

## Features

- Reads UTF-8 CSV files and renders aligned Markdown tables
- Detects numeric columns and right-aligns them automatically
- Preserves unicode text and quoted commas
- Supports `--sort`, `--sort-desc`, `--filter`, `--output`, and `--max-width`
- Handles empty rows, missing values, missing files, and CSVs without headers

## Usage

Run from this directory:

```bash
python3 -m table_formatter input.csv
```

Examples:

```bash
python3 -m table_formatter input.csv --sort Name
python3 -m table_formatter input.csv --sort-desc Salary
python3 -m table_formatter input.csv --filter "Age>=30"
python3 -m table_formatter input.csv --max-width 20
python3 -m table_formatter input.csv --output table.md
```

## Development

Run the provided benchmark tests from the repository root:

```bash
cd ../../..
python3 -m pytest challenges/level-1-table-formatter/test_suite -v
```

Run the agent-authored tests from this solution directory:

```bash
python3 -m pytest tests -v
```

## Notes

- Headers are rendered in bold markdown for readability.
- Integer-like values with leading zeroes, such as zip codes, remain left-aligned text.
