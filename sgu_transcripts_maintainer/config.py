import importlib.resources
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

# General
LOG_LEVEL = os.getenv("LOG_LEVEL", "DEBUG")

# Sentry
SENTRY_DSN = os.getenv("SENTRY_DSN")

# Wiki
WIKI_USERNAME = os.environ["WIKI_USERNAME"]
WIKI_PASSWORD = os.environ["WIKI_PASSWORD"]
WIKI_BASE_URL = "https://www.sgutranscripts.org"
WIKI_REST_BASE_URL = "https://www.sgutranscripts.org/w/rest.php/v1/page/"
WIKI_API_BASE_URL = "https://sgutranscripts.org/w/api.php"

# Internal data paths
DATA_FOLDER = Path(str(importlib.resources.files("sgu_transcripts_maintainer") / "data"))
TEMPLATES_FOLDER = DATA_FOLDER / "templates"
