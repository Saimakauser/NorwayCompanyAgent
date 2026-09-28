import json
import sys

from agent.collector import fetch_company
from agent.verifier import verify_company
from agent.extractor import extract_profile


def run_agent(org_number: str) -> dict:
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

    if len(sys.argv) != 2:
        print(
            "Usage: python app.py "
            "<norwegian_organisation_number>"
        )
        sys.exit(1)

    org_number = sys.argv[1]

    try:
        result = run_agent(org_number)

        print(
            json.dumps(
                result,
                indent=2,
                ensure_ascii=False
            )
        )

    except Exception as error:
        print(f"ERROR: {error}")
        sys.exit(1)