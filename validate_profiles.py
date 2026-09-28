import json

FILE = "data/profiles.jsonl"

total = 0
valid = 0
invalid = 0
duplicates = 0

seen = set()

with open(
    FILE,
    "r",
    encoding="utf-8"
) as file:

    for line_number, line in enumerate(
        file,
        start=1
    ):

        try:
            profile = json.loads(line)
        except json.JSONDecodeError:
            print(
                f"Invalid JSON at line {line_number}"
            )
            invalid += 1
            continue

        total += 1

        org_number = profile.get(
            "organisation_number"
        )

        company_name = profile.get(
            "company_name"
        )

        source = profile.get(
            "source"
        )

        retrieved_at = profile.get(
            "retrieved_at"
        )

        if org_number in seen:
            duplicates += 1
            continue

        seen.add(org_number)

        if (
            org_number
            and company_name
            and source
            and retrieved_at
        ):
            valid += 1
        else:
            invalid += 1
            print(
                f"Missing required field at line "
                f"{line_number}: {org_number}"
            )


print()
print("Dataset validation complete.")
print(f"Total records: {total}")
print(f"Valid records: {valid}")
print(f"Invalid records: {invalid}")
print(f"Duplicate organisation numbers: {duplicates}")