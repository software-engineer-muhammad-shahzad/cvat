# Plan: Annotation Analytics

Start time: 2026-11-23 17:00 PKT. Deadline: 2026-11-24 01:00 PKT.

## Environment
- CVAT commit: d4d08dedb5ad7c5e980c0bc7319a7f5587365dad (branch dev-test01)
- Machine: AMD Ryzen 5 PRO 5650U, 16 GB RAM (15 GB usable), Windows 11 Pro, Docker Desktop
- Data: COCO 2017 val, first 500 images by file name, 3541 annotations, 80 labels. Task #1.
  Subset made with a small script kept outside the repo.

## Order of work (8 hours)
| # | Step | Time |
|---|------|------|
| 1 | Read engine models: how Task, Segment, Job, LabeledShape and Label connect | 0:30 |
| 2 | Backend: new Django app `cvat.apps.test`, endpoint returning per-label counts for a task | 1:30 |
| 3 | Auth: reject anonymous (401) and users without task access (403), using CVAT's TaskPermission | 0:45 |
| 4 | Frontend: new page with bar chart (react-chartjs-2, already a dependency), empty and error states | 2:00 |
| 5 | Speed objective: measure endpoint 5 times, report median and spread | 0:45 |
| 6 | Filter: counts for a single job (`?job=<id>`) | 0:45 |
| 7 | Finish docs, Definition of Done evidence, PR, recording | 1:15 |

## Approach
Count in the database with a single GROUP BY on LabeledShape joined to Label,
filtered by task through job and segment. No Python loops over shapes.

## Decided to skip
- Items 8 and 9 (live updates over WebSocket, reconnect). CVAT has no WebSocket
  layer set up. Adding it is larger than the time available.
- Counting tracks (LabeledTrack) and tags (LabeledImage). COCO import creates only shapes.

## Changes to this plan
- Step 6 changed from a job filter to a frame range filter (start_frame, stop_frame).
  Task #1 has a single job covering all 500 frames, so a job filter would always
  return the same numbers as no filter. A frame range answers a real question:
  what is labelled in one batch of frames.
- Building images from source with docker-compose.dev.yml, but starting the stack with
  the base file only: the dev file publishes the DB port 5432, which Windows blocks.
- Error state tested with a missing task (404) and a user without access (403).
  Stopping the backend logs the UI out (CVAT's global behaviour), so it does not
  reach my page's error state.

## Decision record

**Taken:** count in PostgreSQL with one GROUP BY on LabeledShape joined to Label,
filtered by task through job and segment (cvat/apps/test/views.py).

**Rejected:** reuse CVAT's existing annotation loading (the dataset_manager code behind
GET /api/tasks/{id}/annotations), load every shape into Python and count there.

**What rejecting it cost:**
- I only count shapes (LabeledShape). Tracks (LabeledTrack) and tags (LabeledImage) are not
  counted, because CVAT's loader handles them for me and my query does not. COCO import only
  creates shapes, so the numbers are correct for this data, but a video task with tracks
  would be undercounted.
- My endpoint does not follow CVAT's ViewSet and PolicyEnforcer pattern. I check access
  with TaskPermission by hand, so if CVAT changes how task access works, this view has to
  be updated separately.

**What it bought:** one query instead of loading about 4,000 shape objects, median 43.5 ms
(MO-1), and the count stays fast as tasks grow.
