# Copyright (C) CVAT.ai Corporation
#
# SPDX-License-Identifier: MIT

from django.db.models import Count
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cvat.apps.engine.models import LabeledShape, Task
from cvat.apps.engine.permissions import TaskPermission


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

        rows = (
            LabeledShape.objects.filter(job__segment__task_id=task.id, parent__isnull=True)
            .values("label__name")
            .annotate(count=Count("id"))
            .order_by("-count", "label__name")
        )
        counts = [{"label": row["label__name"], "count": row["count"]} for row in rows]

        return Response(
            {
                "task_id": task.id,
                "total": sum(item["count"] for item in counts),
                "counts": counts,
            }
        )
