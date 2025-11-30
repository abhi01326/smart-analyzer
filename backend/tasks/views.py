import json
from datetime import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Task
from .scoring import calculate_scores


WEIGHT_MODES = {
    "smart":   {"urgency":0.4, "importance":0.4, "effort":0.1, "dependency":0.1},
    "fastest": {"urgency":0.1, "importance":0.1, "effort":0.7, "dependency":0.1},
    "impact":  {"urgency":0.1, "importance":0.8, "effort":0.05, "dependency":0.05},
    "deadline":{"urgency":0.8, "importance":0.1, "effort":0.05, "dependency":0.05},
}


# CREATE
@csrf_exempt
def create_task(request):
    if request.method != "POST":
        return JsonResponse({"error":"Use POST"}, status=405)

    data = json.loads(request.body)

    t = Task.objects.create(
        title=data["title"],
        due_date=datetime.strptime(data["due_date"], "%Y-%m-%d").date(),
        estimated_hours=data["estimated_hours"],
        importance=data["importance"],
        dependencies=data.get("dependencies", [])
    )

    return JsonResponse({"message":"Task created", "id": t.id})


# LIST
def list_tasks(request):
    tasks = Task.objects.all()
    return JsonResponse({
        "tasks": [
            {
                "id": t.id,
                "title": t.title,
                "due_date": t.due_date,
                "estimated_hours": t.estimated_hours,
                "importance": t.importance,
                "dependencies": t.dependencies,
            }
            for t in tasks
        ]
    })


# GET ONE
def get_task(request, task_id):
    try:
        t = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error":"Not found"}, status=404)

    return JsonResponse({
        "id": t.id,
        "title": t.title,
        "due_date": t.due_date,
        "estimated_hours": t.estimated_hours,
        "importance": t.importance,
        "dependencies": t.dependencies,
    })


# UPDATE
@csrf_exempt
def update_task(request, task_id):
    if request.method != "PUT":
        return JsonResponse({"error":"Use PUT"}, status=405)

    data = json.loads(request.body)

    try:
        t = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error":"Not found"}, status=404)

    t.title = data.get("title", t.title)
    if "due_date" in data:
        t.due_date = datetime.strptime(data["due_date"], "%Y-%m-%d").date()
    t.estimated_hours = data.get("estimated_hours", t.estimated_hours)
    t.importance = data.get("importance", t.importance)
    t.dependencies = data.get("dependencies", t.dependencies)

    t.save()
    return JsonResponse({"message":"Task updated"})


# DELETE
@csrf_exempt
def delete_task(request, task_id):
    if request.method != "DELETE":
        return JsonResponse({"error":"Use DELETE"}, status=405)
    try:
        t = Task.objects.get(id=task_id)
    except Task.DoesNotExist:
        return JsonResponse({"error":"Not found"}, status=404)
    t.delete()
    return JsonResponse({"message":"Task deleted"})


# ANALYZE
@csrf_exempt
def analyze_tasks(request):
    mode = request.GET.get("mode", "smart")
    weights = WEIGHT_MODES.get(mode, WEIGHT_MODES["smart"])

    tasks = [
        {
            "id": t.id,
            "title": t.title,
            "due_date": t.due_date,
            "estimated_hours": t.estimated_hours,
            "importance": t.importance,
            "dependencies": t.dependencies,
        }
        for t in Task.objects.all()
    ]

    scored = calculate_scores(tasks, weights)
    return JsonResponse({"tasks": scored})


# TOP 3 SUGGESTIONS
@csrf_exempt
def suggest_tasks(request):
    tasks = [
        {
            "id": t.id,
            "title": t.title,
            "due_date": t.due_date,
            "estimated_hours": t.estimated_hours,
            "importance": t.importance,
            "dependencies": t.dependencies,
        }
        for t in Task.objects.all()
    ]
    scored = calculate_scores(tasks, WEIGHT_MODES["smart"])
    return JsonResponse({"suggestions": scored[:3]})
