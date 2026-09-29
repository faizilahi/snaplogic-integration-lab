import json
from pathlib import Path
import numpy as np
RNG=np.random.default_rng(10)
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/"data"; DATA.mkdir(parents=True, exist_ok=True)
path=DATA/"api_events.jsonl"
with path.open("w",encoding="utf-8") as f:
  for i in range(1,121):
    rec={"event_id":f"EVT{i}","account_id":f"A{int(RNG.integers(1,40))}","status":200 if RNG.random()>0.1 else 429,
      "payload":{"amount":round(float(RNG.uniform(10,200)),2)}}
    f.write(json.dumps(rec)+"\n")
print("Wrote SnapLogic events")

