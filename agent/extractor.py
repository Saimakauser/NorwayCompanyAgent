def extract_profile(record: dict) -> dict:
    raw = record["raw"]

    organisation_form = (
        raw.get("organisasjonsform") or {}
    )

    industry = (
        raw.get("naeringskode1") or {}
    )

    return {
        "organisation_number": str(
            raw.get("organisasjonsnummer", "")
        ),

        "company_name": raw.get("navn"),

        "organisation_form": organisation_form.get(
            "beskrivelse"
        ),

        "organisation_form_code": organisation_form.get(
            "kode"
        ),

        "registration_date": raw.get(
            "registreringsdatoEnhetsregisteret"
        ),

        "number_of_employees": raw.get(
            "antallAnsatte"
        ),

        "industry_code": industry.get("kode"),

        "industry_description": industry.get(
            "beskrivelse"
        ),

        "website": raw.get("hjemmeside"),

        "phone": raw.get("telefon"),

        "email": raw.get("epostadresse"),

        "address": raw.get(
            "forretningsadresse"
        ),

        "retrieved_at": record["retrieved_at"],

        "source": record["source"]
    }