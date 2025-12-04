import csv, os, sys

TERMINATED = 'data/terminated_users_sample.csv'
INVENTORY  = 'data/identity_inventory_sample.csv'
TO_DISABLE = 'data/to_disable.csv'
NOT_FOUND  = 'data/not_found.csv'

def ensure_file(path, hint):
    if not os.path.exists(path):
        sys.exit(f"ERROR: Missing {path}. {hint}")

def main():
    os.makedirs('data', exist_ok=True)

    ensure_file(TERMINATED, "Create data/terminated_users_sample.csv first.")
    ensure_file(INVENTORY,  "Create data/identity_inventory_sample.csv first.")

    # Load terminated emails
    term_emails = set()
    with open(TERMINATED, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            term_emails.add(row['email'].strip().lower())

    # Match against inventory
    found_rows, missing_rows = [], []
    with open(INVENTORY, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    # Build found list ONLY for terminated users (not the inverse)
    for row in rows:
        email = row['email'].strip().lower()
        if email in term_emails:
            found_rows.append(row)

    # Users in terminated list but not found in inventory:
    inventory_emails = {r['email'].strip().lower() for r in rows}
    for email in term_emails:
        if email not in inventory_emails:
            missing_rows.append({'email': email, 'sam_account_name': '', 'source_system': '', 'active': '', 'ad_groups': ''})

    # Write outputs
    fieldnames = ['email','sam_account_name','source_system','active','ad_groups']
    with open(TO_DISABLE, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in found_rows:
            w.writerow({k: r.get(k,'') for k in fieldnames})

    with open(NOT_FOUND, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in missing_rows:
            w.writerow(r)

    print(f"✅ Users to disable: {len(found_rows)} | Not found in directory: {len(missing_rows)}")
    print(f"   Wrote {TO_DISABLE} and {NOT_FOUND}")

if __name__ == "__main__":
    main()
