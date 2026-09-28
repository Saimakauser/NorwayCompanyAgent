import json
import time
import requests

from agent.collector import fetch_company
from agent.verifier import verify_company
from agent.extractor import extract_profile


LIST_URL = "https://data.brreg.no/enhetsregisteret/api/enheter"
OUTPUT_FILE = "data/profiles.jsonl"

BATCH_SIZE = 1000
TARGET_PROFILES = 1000


def get_company_numbers(page=0):
    response = requests.get(
        LIST_URL,
        params={
            "page": page,
            "size": BATCH_SIZE,
            "sort": "organisasjonsnummer,ASC"
        },
        headers={
            "Accept": "application/vnd.brreg.enhetsregisteret.enhet.v2+json"
        },
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    companies = data.get(
        "_embedded",
        {}
    ).get(
        "enheter",
        []
    )

    return [
        str(company["organisasjonsnummer"])
        for company in companies
        if company.get("organisasjonsnummer")
    ]


def load_existing_numbers():
    existing = set()

    try:
        with open(
            OUTPUT_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            for line in file:
                try:
                    profile = json.loads(line)

                    number = profile.get(
                        "organisation_number"
                    )

                    if number:
                        existing.add(str(number))

                except json.JSONDecodeError:
                    continue

    except FileNotFoundError:
        pass

    return existing


def build_one_profile(org_number):
    record = fetch_company(org_number)

    verification = verify_company(
        record,
        org_number
    )

    if not verification["verified"]:
        raise ValueError(
            "Company verification failed."
        )

    return extract_profile(record)


if __name__ == "__main__":

    existing_numbers = load_existing_numbers()

    print(
        f"Existing profiles: {len(existing_numbers)}"
    )

    successful = len(existing_numbers)
    failed = 0
    page = 0

    with open(
        OUTPUT_FILE,
        "a",
        encoding="utf-8"
    ) as output:

        while successful < TARGET_PROFILES:

            print(
                f"\nFetching company list page {page}..."
            )

            try:
                company_numbers = get_company_numbers(
                    page
                )

            except Exception as error:
                print(
                    f"Could not fetch company list: {error}"
                )
                time.sleep(5)
                continue

            if not company_numbers:
                print("No more companies available.")
                break

            for org_number in company_numbers:

                if successful >= TARGET_PROFILES:
                    break

                if org_number in existing_numbers:
                    continue

                try:
                    profile = build_one_profile(
                        org_number
                    )

                    output.write(
                        json.dumps(
                            profile,
                            ensure_ascii=False
                        )
                        + "\n"
                    )

                    output.flush()

                    existing_numbers.add(
                        org_number
                    )

                    successful += 1

                    print(
                        f"[{successful}/{TARGET_PROFILES}] "
                        f"OK - {org_number} - "
                        f"{profile.get('company_name')}"
                    )

                except Exception as error:

                    failed += 1

                    print(
                        f"FAILED - {org_number} - {error}"
                    )

                time.sleep(0.05)

            page += 1

    print()
    print("Collection complete.")
    print(f"Total successful profiles: {successful}")
    print(f"Failures during this run: {failed}")
    print(f"Saved to: {OUTPUT_FILE}")