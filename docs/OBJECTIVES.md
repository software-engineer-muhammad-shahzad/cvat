# Objectives

## Machine
AMD Ryzen 5 PRO 5650U, 16 GB RAM (15 GB usable), Windows 11 Pro, Docker Desktop.
CVAT commit d4d08dedb5ad7c5e980c0bc7319a7f5587365dad.

## MO-1
| Field | Entry |
|---|---|
| What is measured | Server response time of GET /api/test/tasks/1/annotation-counts |
| How | `curl.exe -w "%{time_total}"`, logged in as admin, 5 runs after one warm-up request |
| Target | Median of 5 runs at or below 200 ms |
| Conditions | Local Docker stack, Task #1 (500 images, 3541 annotations), nothing else running |
| Not included | First request after a server restart; browser rendering time |

Why 200 ms: the count is a single SQL query, so it should return quickly. If it does
not, the query or its indexes need work, and the measurement will show that.

## Results
Measured 2026-11-23, token auth (one login, token reused), 1 warm-up request then 5 timed runs.

```
200 0.054183
200 0.044029
200 0.043543
200 0.041822
200 0.043300
median_ms=43.5 min_ms=41.8 max_ms=54.2
```

**Median 43.5 ms, spread 41.8 to 54.2 ms. Target met.**

The target turned out generous: the endpoint is one GROUP BY query over about 4,000 shape rows. I measured with a token because Basic auth re-hashes the password on every request, which adds a fixed cost unrelated to the endpoint.
