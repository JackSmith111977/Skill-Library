---
name: data-validator
description: >
  This skill should be used when the user asks to "validate data",
  "check data quality", "verify data format", "run data validation",
  or "ensure data integrity".
version: 0.1.0
allowed-tools: [Bash, Read, Write]
---

# Data Validator

Validates data files for format, schema, and quality issues.

## Usage

Describe the data format and validation rules. The skill will generate a validation report.

### Supported Formats

- CSV, JSON, YAML, XML
- Custom schema validation
- Data quality metrics

### Validation Types

- **Schema check**: field types, required fields, value ranges
- **Format check**: encoding, delimiters, line endings
- **Quality check**: null values, duplicates, outliers
