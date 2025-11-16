# CSV Data Quality Checker (Mini Version)

A very small Python script that performs basic data-quality checks on a
`customers.csv` file:

- Counts how many rows are missing a **name**
- Counts how many rows are missing an **email**
- Counts how many rows have an **invalid email format**

This is a minimal example for working with CSV files and data quality checks.

---

## Example CSV format

The script expects a file at `data/customers.csv` with at least the columns:

```csv
customer_id,name,email
1,Alice Smith,alice@example.com
2,Bob,bob.example.com
3,,no-name@example.com
4,Charlie,charlie@
5,David,
6,,