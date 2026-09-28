def verify_company(record: dict, requested_org_number: str) -> dict:
    requested_org_number = str(
        requested_org_number
    ).strip()

    raw = record["raw"]

    returned_number = str(
        raw.get("organisasjonsnummer", "")
    ).strip()

    if returned_number != requested_org_number:
        raise ValueError(
            "Identity verification failed: "
            "organisation numbers do not match."
        )

    return {
        "verified": True,
        "organisation_number": returned_number
    }