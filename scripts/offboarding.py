import csv, os, sys

TO_DISABLE = 'data/to_disable.csv'

def main():
    if not os.path.exists(TO_DISABLE):
        sys.exit("ERROR: data/to_disable.csv not found. Run scripts/identity_validation.py first.")

    print("🔧 Simulating offboarding workflow...")
    with open(TO_DISABLE, newline='') as f:
        reader = csv.DictReader(f)
        count = 0
        for row in reader:
            email = row.get('email') or row.get('Email') or 'UNKNOWN'
            print(f"Disabling account for: {email}")
            print(f"Revoking MFA for: {email}")
            count += 1

    print(f"✅ Offboarding simulation complete. Processed {count} user(s).")

if __name__ == "__main__":
    main()
