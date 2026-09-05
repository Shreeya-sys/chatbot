from urllib.parse import urlparse

from config import TRUSTED_WEB_DOMAINS


def is_trusted_url(url: str) -> bool:
    host = urlparse(url).netloc.lower()
    return any(host == domain or host.endswith("." + domain) for domain in TRUSTED_WEB_DOMAINS)


def trusted_search_placeholder(query: str) -> list[dict]:
    """
    Placeholder for Stage 9. Add Tavily, SerpAPI, or another search provider here.
    Keep filtering through is_trusted_url before evidence reaches the LLM.
    """
    return []
