"""Single source of truth for product branding and project identity.

To rename the product, change ONLY this file + pyproject.toml [project].name
+ the rootine/ directory name. Everything else reads from here.

To change the advisor (human owner) name, update ADVISOR_NAME and
ADVISOR_EMAIL below. All Python code reads from here.
"""

NAME = "SpecAg"
NAME_LOWER = "specag"
TAGLINE = "Run an AI engineering team with full cost control and traceability."
DESCRIPTION = f"{NAME} — {TAGLINE}"
WEBSITE = "https://specag.com"
GITHUB = "https://github.com/dedeepyasai/specag"
GITHUB_SHORT = "dedeepyasai/specag"

ADVISOR_NAME = "Datta"
ADVISOR_EMAIL = "sai.gondi@ieee.org"
