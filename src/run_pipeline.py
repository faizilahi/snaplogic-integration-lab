import json, sys
from pathlib import Path
import pandas as pd
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from throttle import fetch_page, ThrottleError
from error_queue import ErrorQueue
DATA, OUT = ROOT / "data", ROOT / "output"
OUT.mkdir(parents=True, exist_ok=True)

def main():
    blob = json.loads((DATA / "api_pages.json").read_text(encoding="utf-8"))
    pages, throttle = blob["pages"], set(blob["throttle_pages"])
    q = ErrorQueue()
    loaded = []
    # naive run: on 429, queue page and continue without retry
    for i in range(len(pages)):
        try:
            loaded.extend(fetch_page(pages, i, throttle, attempt=0))
        except ThrottleError as e:
            q.push(e.page, "HTTP_429")
    incomplete = len(loaded)
    peak = q.depth()
    # drain with retry
    for item in q.drain():
        loaded.extend(fetch_page(pages, item["page_idx"], throttle, attempt=1))
    summary = {
        "total_pages": len(pages),
        "throttled_pages": peak,
        "incomplete_shipments": incomplete,
        "after_queue_drain": len(loaded),
        "under_count": len(loaded) - incomplete,
    }
    pd.DataFrame(loaded).to_csv(OUT / "shipments_loaded.csv", index=False)
    pd.DataFrame([summary]).to_csv(OUT / "pipeline_summary.csv", index=False)
    print(json.dumps(summary, indent=2))
if __name__ == "__main__":
    main()
