import json
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"output"; OUT.mkdir(parents=True, exist_ok=True)
rows=[]; errors=[]
with (ROOT/"data"/"api_events.jsonl").open(encoding="utf-8") as f:
  for line in f:
    rec=json.loads(line)
    if rec["status"]==429:
      errors.append({**rec,"error":"rate_limited"}); continue
    rows.append({"event_id":rec["event_id"],"account_id":rec["account_id"],"amount":rec["payload"]["amount"]})
loaded=pd.DataFrame(rows).drop_duplicates("event_id")
loaded.to_csv(OUT/"warehouse_events.csv",index=False)
pd.DataFrame(errors).to_csv(OUT/"error_queue.csv",index=False)
pd.DataFrame([{"loaded":len(loaded),"errors":len(errors)}]).to_csv(OUT/"summary.csv",index=False)
print(pd.read_csv(OUT/"summary.csv"))

