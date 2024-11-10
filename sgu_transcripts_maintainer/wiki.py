from functools import cache
from http.client import NOT_FOUND
from typing import TYPE_CHECKING

import pywikibot
from requests import RequestException

from sgu_transcripts_maintainer.config import (
    WIKI_API_BASE_URL,
    WIKI_BASE_URL,
    WIKI_PASSWORD,
    WIKI_REST_BASE_URL,
    WIKI_USERNAME,
)
from sgu_transcripts_maintainer.global_logger import logger

if TYPE_CHECKING:
    from requests import Session


# region public functions
def episode_has_wiki_page(client: "Session", episode_number: int) -> bool:
    """Check if an episode has a wiki page.

    Args:
        client (Session): The HTTP client session.
        episode_number (int): The episode number.

    Returns:
        bool: True if the episode has a wiki page, False otherwise.
    """
    resp = client.get(WIKI_REST_BASE_URL + str(episode_number))

    if resp.status_code == NOT_FOUND:
        return False

    resp.raise_for_status()

    return True


@cache
def log_into_wiki(client: "Session") -> str:
    """Perform a login to the wiki and return the csrf token."""
    login_token = _get_login_token(client)
    _send_credentials(client, login_token)

    return _get_csrf_token(client)


def create_page(
    client: "Session",
    page_title: str,
    page_text: str,
    *,
    allow_page_editing: bool,
) -> None:
    """Create a wiki page."""
    csrf_token = log_into_wiki(client)

    payload = {
        "action": "edit",
        "title": page_title,
        "summary": "Page created (or rewritten) by transcription-bot. https://github.com/mheguy/transcription-bot",
        "format": "json",
        "text": page_text,
        "notminor": True,
        "bot": True,
        "token": csrf_token,
        "createonly": True,
    }

    if allow_page_editing:
        payload.pop("createonly")

    resp = client.post(WIKI_API_BASE_URL, data=payload)
    resp.raise_for_status()
    data = resp.json()

    if "error" in data:
        raise RequestException("Error during page creation: %s", data["error"])

    logger.debug(data)


def get_wiki_page(name: str) -> pywikibot.Page:
    """Retrieve the wiki page with the given name."""
    site = pywikibot.Site(url=WIKI_BASE_URL)
    return pywikibot.Page(site, name)


# endregion
# region private functions
def _get_login_token(client: "Session") -> str:
    params = {"action": "query", "meta": "tokens", "type": "login", "format": "json"}

    resp = client.get(url=WIKI_API_BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    return data["query"]["tokens"]["logintoken"]


def _send_credentials(client: "Session", login_token: str) -> None:
    payload = {
        "action": "login",
        "lgname": WIKI_USERNAME,
        "lgpassword": WIKI_PASSWORD,
        "lgtoken": login_token,
        "format": "json",
    }

    resp = client.post(WIKI_API_BASE_URL, data=payload)
    resp.raise_for_status()

    if resp.json()["login"]["result"] != "Success":
        raise ValueError(f"Login failed: {resp.json()}")


def _get_csrf_token(client: "Session") -> str:
    params = {"action": "query", "meta": "tokens", "format": "json"}

    resp = client.get(url=WIKI_API_BASE_URL, params=params)
    resp.raise_for_status()
    data = resp.json()

    return data["query"]["tokens"]["csrftoken"]


# endregion
