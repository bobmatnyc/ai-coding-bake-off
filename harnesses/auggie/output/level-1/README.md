# table_formatter

A Python tool that converts CSV files into beautifully formatted Markdown tables. Handles unicode, numeric alignment, sorting, filtering, and more.

## Usage

```bash
# Basic usage
python3 -m table_formatter input.csv

# Sort ascending by a column
python3 -m table_formatter input.csv --sort Name

# Sort descending
python3 -m table_formatter input.csv --sort-desc Salary

# Filter rows
python3 -m table_formatter input.csv --filter "Age>30"
python3 -m table_formatter input.csv --filter "City=NYC"
python3 -m table_formatter input.csv --filter "Salary>=80000"

# Write to file
python3 -m table_formatter input.csv --output table.md

# Truncate long cells
python3 -m table_formatter input.csv --max-width 20
```

## Features

- **Auto-alignment**: Numeric columns right-aligned, text columns left-aligned
- **Zip code safety**: Leading-zero values (e.g. `01234`) treated as text
- **Unicode support**: Handles emoji, CJK, accented characters
- **Missing values**: Empty cells handled gracefully
- **Sorting**: Ascending (`--sort`) or descending (`--sort-desc`) by any column
- **Filtering**: Expressions like `age>30`, `name=Alice`, `salary>=50000`
- **Output file**: Write to a file with `--output`
- **Max width**: Truncate long cells with `--max-width N`

## Supported Filter Operators

| Operator | Meaning |
|:---------|:--------|
| `=` | Equal |
| `!=` | Not equal |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |

## Example

Input (`sales.csv`):
```
Product,Q1 Sales,Region
Widget A,15234,North America
Widget B,8921,Europe
```

Output:
```
| Product  | Q1 Sales | Region        |
|:---------|--------:|:--------------|
| Widget A |   15234 | North America |
| Widget B |    8921 | Europe        |
```

## Library Usage

```python
from table_formatter import parse_csv, detect_column_types, format_table

headers, rows = parse_csv("data.csv")
col_types = detect_column_types(headers, rows)
markdown = format_table(headers, rows, col_types, max_width=50)
print(markdown)
```

## Running Tests

```bash
# Provided test suite
python3 -m pytest ../../../../challenges/level-1-table-formatter/test_suite/ -v

# Additional tests
python3 -m pytest tests/ -v
```

## Requirements

- Python 3.12+
- No external dependencies (stdlib only)
