import time
import requests
from datetime import datetime, timezone

BASE_URL = "https://data.brreg.no/enhetsregisteret/api"


def fetch_company(org_number: str) -> dict:
    org_number = str(org_number).strip()

    if not org_number.isdigit() or len(org_number) != 9:
        raise ValueError(
            "Organisation number must contain exactly 9 digits."
        )

    url = f"{BASE_URL}/enheter/{org_number}"

    last_error = None

    for attempt in range(5):
        try:
            response = requests.get(
                url,
                headers={"Accept": "application/json"},
                timeout=30
            )

            if response.status_code == 404:
                raise ValueError(
                    f"Company {org_number} was not found."
                )

            if response.status_code == 410:
                raise ValueError(
                    f"Company {org_number} is no longer available."
                )

            response.raise_for_status()

            return {
                "organisation_number": org_number,
                "retrieved_at": datetime.now(
                    timezone.utc
                ).isoformat(),
                "source": url,
                "raw": response.json()
            }

        except (
            requests.exceptions.ConnectionError,
            requests.exceptions.Timeout
        ) as error:

            last_error = error

            if attempt < 4:
                wait_time = 2 ** attempt
                time.sleep(wait_time)

    raise last_error