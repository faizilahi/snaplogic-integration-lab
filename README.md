# API Pipeline and the 429 Error Queue

[Faiz Elahi](https://www.linkedin.com/in/faizilahi) — [pendataco.com](https://pendataco.com) — [github.com/faizilahi](https://github.com/faizilahi)

Synthetic data only. No vendor-customer employment claim.

A SnapLogic-style pipeline pulled paginated `/v1/shipments` and melted under
HTTP 429s. Failed pages landed in an error queue; without drain logic the next
run skipped them and under-counted shipments by **640**.

## The pipeline

`pipelines/shipments_api.json` — rest read → paginate → map → write.

## The 429s

Simulator injects **8** throttled pages (80 rows each). Retry-After honored in
`src/throttle.py`.

## The queue

Error queue depth peaked at **8** pages. Draining before the next watermark
advanced restored total shipments to **4,800** (vs incomplete **4,160**).

```powershell
pip install -r requirements.txt
python scripts/generate_synthetic_data.py
python src/run_pipeline.py
```
