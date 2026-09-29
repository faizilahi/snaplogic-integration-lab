from __future__ import annotations

class ThrottleError(Exception):
    def __init__(self, page, retry_after=1):
        self.page = page
        self.retry_after = retry_after

def fetch_page(pages, idx, throttle_pages, attempt=0, max_retries=3):
    if idx in throttle_pages and attempt < 1:
        # first attempt fails with 429
        raise ThrottleError(idx, retry_after=1)
    return pages[idx]
