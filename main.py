import csv
from pathlib import Path

DATA_PATH = Path("data/customers.csv")


def is_missing(value: str | None) -> bool:
    """Return True if value is empty or whitespace."""
    if value is None:
        return True
    return value.strip() == ""


def is_valid_email(email: str | None) -> bool:
    """Very simple email check: must contain '@' and a dot after it."""
    if email is None:
        return False
    email = email.strip()
    if "@" not in email:
        return False
    local, _, domain = email.partition("@")
    if not local or not domain:
        return False
    return "." in domain


def load_customers(path: Path) -> list[dict]:
    """Load customers from a CSV file."""
    rows: list[dict] = []
    with path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows


def analyze_customers(rows: list[dict]) -> dict:
    """Return a simple data-quality summary."""
    total = len(rows)
    missing_name = 0
    missing_email = 0
    invalid_email = 0

    invalid_email_rows: list[dict] = []

    for row in rows:
        name = row.get("name")
        email = row.get("email")

        if is_missing(name):
            missing_name += 1

        if is_missing(email):
            missing_email += 1
        elif not is_valid_email(email):
            invalid_email += 1
            invalid_email_rows.append(row)

    return {
        "total_rows": total,
        "missing_name": missing_name,
        "missing_email": missing_email,
        "invalid_email": invalid_email,
        "invalid_email_rows": invalid_email_rows,
    }


def print_report(summary: dict) -> None:
    """Print a human-readable report."""
    print("=== CSV Data Quality Report ===\n")
    print(f"Total rows        : {summary['total_rows']}")
    print(f"Missing 'name'    : {summary['missing_name']}")
    print(f"Missing 'email'   : {summary['missing_email']}")
    print(f"Invalid 'email'   : {summary['invalid_email']}")
    print()

    if summary["invalid_email_rows"]:
        print("Rows with invalid email:")
        for row in summary["invalid_email_rows"]:
            cid = row.get("customer_id", "").strip()
            email = (row.get("email") or "").strip()
            print(f"  - customer_id={cid!r}, email={email!r}")
    else:
        print("No invalid email addresses found.")

    print()


def main() -> None:
    if not DATA_PATH.exists():
        print(f"CSV file not found: {DATA_PATH}")
        return

    rows = load_customers(DATA_PATH)
    if not rows:
        print("No rows found in CSV file.")
        return

    summary = analyze_customers(rows)
    print_report(summary)


if __name__ == "__main__":
    main()