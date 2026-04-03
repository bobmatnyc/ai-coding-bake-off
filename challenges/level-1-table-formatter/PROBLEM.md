# Level 1: Markdown Table Formatter

**Time Budget:** ~30 minutes  
**Difficulty:** Low  
**Focus:** CLI tool, file I/O, string formatting, data type detection

## Problem Statement

Build a Python module that reads CSV files and outputs beautifully formatted Markdown tables.

The tool must handle real-world CSV data gracefully: mixed data types, unicode characters, missing values, and varying column widths. It should be usable both as a CLI tool and as an importable Python module.

## Requirements

### Core Functionality

1. **CSV Reading**: Read standard CSV files (comma-delimited, with headers).
2. **Markdown Output**: Generate properly formatted Markdown tables with aligned columns.
3. **Column Alignment**: Automatically detect column data types and align accordingly:
   - Numeric columns: right-aligned
   - Text columns: left-aligned
   - Mixed columns: left-aligned
4. **Header Formatting**: Bold headers with separator row using proper Markdown alignment syntax (`:---`, `---:`, `:---:`).

### CLI Interface

The tool should run as:

```bash
python3 -m table_formatter input.csv
```

With optional flags:
- `--sort COLUMN` --- Sort rows by the specified column (ascending by default)
- `--sort-desc COLUMN` --- Sort rows by the specified column (descending)
- `--filter EXPRESSION` --- Filter rows by a simple expression (e.g., `"age>30"`, `"name=Alice"`, `"salary>=50000"`)
- `--output FILE` --- Write to file instead of stdout
- `--max-width N` --- Truncate cell content to N characters (with ellipsis)

### Edge Cases to Handle

- Empty CSV files (headers only, no data rows)
- CSV files with no headers
- Unicode characters in data (emoji, CJK, accented characters)
- Missing values (empty cells)
- Very long cell content
- Numeric strings that should remain strings (e.g., zip codes like "01234")
- Quoted fields containing commas

## Example

**Input** (`sales.csv`):
```csv
Product,Q1 Sales,Q2 Sales,Region
Widget A,15234,18902,North America
Widget B,8921,7654,Europe
Gadget X,42100,39877,Asia Pacific
Gadget Y,,12340,North America
```

**Output**:
```markdown
| Product  | Q1 Sales | Q2 Sales | Region        |
|:---------|--------:|--------:|:--------------|
| Widget A |   15234 |   18902 | North America |
| Widget B |    8921 |    7654 | Europe        |
| Gadget X |   42100 |   39877 | Asia Pacific  |
| Gadget Y |         |   12340 | North America |
```

## Deliverables

1. A `table_formatter/` package (or single module) with the core logic
2. CLI entry point via `python3 -m table_formatter`
3. At least 5 additional tests beyond the provided test suite
4. A brief README.md explaining usage

## Open Decisions (Agent's Choice)

- CLI argument parsing approach (argparse, click, typer, etc.)
- Internal data representation
- How to detect numeric vs. text columns
- Error handling strategy for malformed CSV
- Code organization (single file vs. package)

## Evaluation Criteria

See `evaluation/rubric.md` for the full scoring rubric. Key weights for this level:

- **Correctness**: 30%
- **Code Quality**: 25%
- **Testing**: 20%
- **Error Handling**: 15%
- **Documentation**: 10%
