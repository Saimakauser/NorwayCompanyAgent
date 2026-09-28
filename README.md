# Norway Company Information Agent

An agent that retrieves, verifies, and extracts public company information for Norwegian organisations using the official Brønnøysund Register Centre Enhetsregisteret API.

## What the Agent Does

Given a Norwegian organisation number, the agent:

1. Fetches the company record from the official public registry.
2. Verifies that the returned organisation number matches the requested organisation number.
3. Extracts useful company facts.
4. Records the source URL.
5. Records the retrieval timestamp.
6. Can compare a saved profile with a fresh registry record to detect changes.

## Example

Run:

```bash
python app.py 810034882

The agent returns structured JSON containing information such as:

Organisation number
Company name
Organisation form
Registration date
Number of employees
Industry code and description
Website
Phone
Email when available
Address
Source URL
Retrieval timestamp
Dataset

The repository contains:

data/profiles.jsonl

The dataset contains:

1,000 Norwegian organisation profiles
1,000 unique organisation numbers
Verified organisation-number matching
Source URL for every profile
Retrieval timestamp for every profile
No duplicate organisation numbers
Dataset validation: 1,000 valid / 1,000 total
Identity Verification

The agent does not assume that a returned record belongs to the requested company.

For every company:

Requested organisation number
        ↓
Official registry lookup
        ↓
Returned organisation number
        ↓
Exact comparison
        ↓
Verified profile

If the organisation numbers do not match, the profile is rejected.

Update Detection

The update_checker.py script retrieves a fresh company record and compares it against the previously saved profile.

Run:

python update_checker.py

The result reports:

Whether the company changed
Which fields changed
Previous values
Current values
Fresh retrieval timestamp
Source URL
Dataset Validation

Run:

python validate_profiles.py

The validator checks:

Valid JSON
Required fields
Duplicate organisation numbers
Number of valid profiles
Data Source

Primary source:

Brønnøysund Register Centre — Enhetsregisteret public API.

The agent uses public registry information and preserves the source URL for each retrieved company profile.


Installation

Create and activate a Python virtual environment:

python -m venv .venv


Activate on Windows PowerShell:

.venv\Scripts\Activate.ps1


Install dependencies:

pip install -r requirements.txt
Dependencies
Python
requests
pydantic
python-dotenv


No paid external AI model API is required for the current implementation.

Cost

Expected external API cost:

$0

The current implementation uses the public Brønnøysund Register Centre API and does not require a paid LLM or commercial data API.

Actual network usage depends on the number of company records requested.

One-Command Usage



For a single company:

python app.py <norwegian_organisation_number>

Example:

python app.py 810034882

Project Structure

NorwayCompanyAgent/

├── agent/
│   ├── __init__.py
│   ├── collector.py
│   ├── verifier.py
│   └── extractor.py
├── data/
│   └── profiles.jsonl
├── app.py
├── build_profiles.py
├── update_checker.py
├── validate_profiles.py
├── requirements.txt
├── README.md
└── .gitignore

Submission Commit

Exact submission commit:

2fd939532084fefbb718c70ae76588aae5d0b742

Repository

https://github.com/Saimakauser/NorwayCompanyAgent