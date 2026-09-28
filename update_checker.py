import json

from agent.collector import fetch_company
from agent.verifier import verify_company
from agent.extractor import extract_profile


def load_saved_profile(org_number):
    with open(
        "data/profiles.jsonl",
        "r",
        encoding="utf-8"
    ) as file:

        for line in file:

            profile = json.loads(line)

            if (
                str(profile.get("organisation_number"))
                == str(org_number)
            ):
                return profile

    return None


def compare_profiles(old, new):
    changes = {}

    fields = [
        "company_name",
        "organisation_form",
        "organisation_form_code",
        "registration_date",
        "number_of_employees",
        "industry_code",
        "industry_description",
        "website",
        "phone",
        "email",
        "address"
    ]

    for field in fields:

        old_value = old.get(field)
        new_value = new.get(field)

        if old_value != new_value:

            changes[field] = {
                "old": old_value,
                "new": new_value
            }

    return changes


def check_for_updates(org_number):

    old_profile = load_saved_profile(
        org_number
    )

    if old_profile is None:
        raise ValueError(
            f"No saved profile found for {org_number}"
        )

    record = fetch_company(
        org_number
    )

    verification = verify_company(
        record,
        org_number
    )

    if not verification["verified"]:
        raise ValueError(
            "Company verification failed."
        )

    new_profile = extract_profile(
        record
    )

    changes = compare_profiles(
        old_profile,
        new_profile
    )

    return {
        "organisation_number": org_number,
        "checked_at": new_profile[
            "retrieved_at"
        ],
        "source": new_profile[
            "source"
        ],
        "changed": bool(changes),
        "changes": changes
    }


if __name__ == "__main__":

    organisation_number = "810034882"

    result = check_for_updates(
        organisation_number
    )

    print(
        json.dumps(
            result,
            indent=2,
            ensure_ascii=False
        )
    )