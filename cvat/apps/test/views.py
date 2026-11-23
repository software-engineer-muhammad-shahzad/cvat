# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from django.db.models import Count
from rest_framework.exceptions import NotFound, PermissionDenied, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cvat.apps.engine.models import LabeledShape, Task
from cvat.apps.engine.permissions import TaskPermission


def parse_frame_param(request, name):
    value = request.query_params.get(name)
    if value is None:
        return None
    try:
        frame = int(value)
    except ValueError:
        raise ValidationError(f"{name} must be an integer")
    if frame < 0:
        raise ValidationError(f"{name} must not be negative")
    return frame


class AnnotationCountsView(APIView):
    # CVAT's default PolicyEnforcer needs a ViewSet with iam_permission_class,
    # so this view only requires a login and checks task access itself below.
    permission_classes = [IsAuthenticated]

    def get(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            raise NotFound("Task not found")

        if not TaskPermission.create_scope_view(request, task).check_access().allow:
            raise PermissionDenied("You do not have access to this task")

        start_frame = parse_frame_param(request, "start_frame")
        stop_frame = parse_frame_param(request, "stop_frame")
        if start_frame is not None and stop_frame is not None and start_frame > stop_frame:
            raise ValidationError("start_frame must not be greater than stop_frame")

        shapes = LabeledShape.objects.filter(job__segment__task_id=task.id, parent__isnull=True)
        if start_frame is not None:
            shapes = shapes.filter(frame__gte=start_frame)
        if stop_frame is not None:
            shapes = shapes.filter(frame__lte=stop_frame)

        rows = (
            shapes.values("label__name")
            .annotate(count=Count("id"))
            .order_by("-count", "label__name")
        )
        counts = [{"label": row["label__name"], "count": row["count"]} for row in rows]

        return Response(
            {
                "task_id": task.id,
                "start_frame": start_frame,
                "stop_frame": stop_frame,
                "total": sum(item["count"] for item in counts),
                "counts": counts,
            }
        )