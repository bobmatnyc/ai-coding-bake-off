# table_formatter

Converts CSV files to beautifully formatted Markdown tables with automatic column type detection, Unicode support, filtering, and sorting.

## Usage

```bash
python3 -m table_formatter input.csv
```

### Options

| Flag | Description |
|------|-------------|
| `--sort COLUMN` | Sort rows by COLUMN (ascending) |
| `--sort-desc COLUMN` | Sort rows by COLUMN (descending) |
| `--filter EXPRESSION` | Filter rows (e.g. `Age>30`, `Name=Alice`, `Salary>=50000`) |
| `--output FILE` | Write output to FILE instead of stdout |
| `--max-width N` | Truncate cell content to N display columns (appends `…`) |

### Examples

Basic usage:

```bash
python3 -m table_formatter data.csv
```

Sort by a column:

```bash
python3 -m table_formatter data.csv --sort Name
python3 -m table_formatter data.csv --sort-desc Score
```

Filter rows:

```bash
python3 -m table_formatter data.csv --filter "Age>30"
python3 -m table_formatter data.csv --filter "Dept=Engineering"
python3 -m table_formatter data.csv --filter "Salary>=75000"
```

Combine filter and sort, write to file:

```bash
python3 -m table_formatter data.csv --filter "Age>25" --sort Name --output report.md
```

Truncate long cells:

```bash
python3 -m table_formatter data.csv --max-width 20
```

## Output Format

Given a CSV like:

```
Name,Age,City
Alice,32,New York
Bob,25,Los Angeles
```

The output is:

```markdown
| Name  | Age | City        |
| :---- | --: | :---------- |
| Alice |  32 | New York    |
| Bob   |  25 | Los Angeles |
```

- Text columns are left-aligned (`:---`)
- Numeric columns are right-aligned (`---:`)
- CJK and other wide Unicode characters are handled correctly

## Library API

```python
from table_formatter.formatter import read_csv, format_table, sort_rows, apply_filter
from table_formatter.detector import detect_column_types

headers, rows = read_csv("data.csv")

# Optional: filter and sort
rows = apply_filter(rows, headers, "Age>30")
rows = sort_rows(rows, headers, "Name")

alignments = detect_column_types(rows, headers)
table = format_table(headers, rows, alignments, max_width=None)
print(table)
```

### Functions

- `read_csv(path)` - Read CSV and return `(headers, rows)`
- `detect_column_types(rows, headers)` - Return per-column alignment list (`"left"` or `"right"`)
- `format_table(headers, rows, alignments, max_width=None)` - Render Markdown table string
- `apply_filter(rows, headers, expression)` - Filter rows by expression
- `sort_rows(rows, headers, column, descending=False)` - Sort rows by column
- `cell_display_width(text)` - Compute display width accounting for wide Unicode characters
- `truncate_cell(text, max_width)` - Truncate to display width with `…` ellipsis
- `parse_filter_expression(expr)` - Parse filter string into `(column, operator, value)`
- `build_separator_cell(alignment, width)` - Build Markdown separator cell

## Filter Expressions

Supported operators: `>`, `<`, `>=`, `<=`, `=`, `!=`

Numeric comparison is attempted first (using `float()`). Falls back to string comparison if either side is not numeric.

Examples:
- `Age>30` — rows where Age is numerically greater than 30
- `Name=Alice` — rows where Name equals "Alice" (string comparison)
- `Salary!=0` — rows where Salary is not zero
- `Dept!=HR` — rows where Dept is not "HR"
