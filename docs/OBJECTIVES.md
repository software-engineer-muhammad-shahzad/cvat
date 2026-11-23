@'
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
(Raw output pasted here after measuring.)
'@ | Set-Content -Encoding UTF8 D:\cvat\docs\OBJECTIVES.md