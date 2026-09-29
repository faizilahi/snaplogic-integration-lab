from pathlib import Path
import json, pandas as pd
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"; DATA.mkdir(parents=True, exist_ok=True)
rows = [{"shipment_id": f"SH{i:05d}", "status": "SHIPPED", "weight_lb": round((i % 50) + 1.5, 2)} for i in range(4800)]
# 60 pages of 80
pages = [rows[i:i+80] for i in range(0, 4800, 80)]
# mark 8 pages as 429
throttle_pages = list(range(10, 18))
(DATA / "api_pages.json").write_text(json.dumps({"pages": pages, "throttle_pages": throttle_pages}), encoding="utf-8")
print("pages", len(pages), "throttled", throttle_pages)
