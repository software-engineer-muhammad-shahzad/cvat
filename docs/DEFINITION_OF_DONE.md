# \# Definition of Done

# 

# Written before implementation, ticked at the end. Every tick has evidence beside it.

# 

# \- \[x] \*\*Endpoint returns correct counts.\*\*

# &#x20; `GET /api/test/tasks/1/annotation-counts` returns `"total":3953` across 78 labels

# &#x20; (person 1217, chair 227, car 195, ...).

# &#x20; Checked against the source file: the COCO subset has 3541 objects, but CVAT stores each

# &#x20; polygon part of a multi-part object as its own shape. Counting polygon parts in

# &#x20; `instances\_val2017\_500.json` gives exactly 3953.

# \- \[x] \*\*No login returns 401.\*\*

# &#x20; ```

# &#x20; curl.exe -i http://localhost:8080/api/test/tasks/1/annotation-counts

# &#x20; HTTP/1.1 401 Unauthorized

# &#x20; {"detail":"Authentication credentials were not provided."}

# &#x20; ```

# \- \[x] \*\*User without access to the task returns 403.\*\*

# &#x20; ```

# &#x20; curl.exe -i -u usertwo:\*\*\* http://localhost:8080/api/test/tasks/1/annotation-counts

# &#x20; HTTP/1.1 403 Forbidden

# &#x20; {"detail":"You do not have access to this task"}

# &#x20; ```

# &#x20; Same message in the UI: \[error-403.png](evidence/error-403.png)

# \- \[x] \*\*Page shows bar chart for task #1.\*\* \[chart.png](evidence/chart.png)

# &#x20; Reached from the task's Actions menu, "Annotation counts".

# \- \[x] \*\*Page shows a "no annotations" message for an empty task.\*\* \[empty.png](evidence/empty.png)

# \- \[x] \*\*Page shows an error message when the request fails.\*\* \[error-404.png](evidence/error-404.png)

# &#x20; Task 99999 returns 404 "Task not found", shown with a Retry button.

# \- \[x] \*\*MO-1 measured, 5 runs, raw output saved.\*\* See \[OBJECTIVES.md](OBJECTIVES.md).

# \- \[x] \*\*MO-1 target met.\*\* Median 43.5 ms against a target of 200 ms (spread 41.8 to 54.2 ms).

# \- \[x] \*\*Filter returns counts for a frame range only.\*\* (Changed from a job filter, see Plan.)

# &#x20; `?start\_frame=0\&stop\_frame=99` returns `"total":797`. Counting polygon parts for the first

# &#x20; 100 images of the subset gives exactly 797.

# &#x20; `?start\_frame=50\&stop\_frame=10` returns 400 `\["start\_frame must not be greater than stop\_frame"]`.

# &#x20; `?start\_frame=abc` returns 400 `\["start\_frame must be an integer"]`.

# \- \[x] \*\*Everything not finished is listed below.\*\*

# 

# \## Not finished

# 

# \- \*\*Item 8, live updates over WebSocket.\*\* Not started. CVAT runs on ASGI (uvicorn) but has no

# &#x20; WebSocket routing or Channels layer. Adding one means a new dependency, a channel layer on

# &#x20; Redis, and a signal on shape changes. I judged it larger than the time left after items 1 to 7.

# \- \*\*Item 9, reconnect after a dropped connection.\*\* Depends on item 8.

# \- \*\*Frame range filter in the UI.\*\* The API supports it; the page always shows the whole task.

# \- \*\*Tracks and tags are not counted\*\*, only shapes. Correct for COCO data, not for video

# &#x20; tasks with tracks. See the decision record in the Plan.

