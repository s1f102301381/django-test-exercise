from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import make_aware
from django.utils.dateparse import parse_datetime
from django.http import Http404

from todo.models import Task


def index(request):
    if request.method == 'POST':
        due_at_value = request.POST.get('due_at')
        due_at = None
        if due_at_value:
            due_at = make_aware(parse_datetime(due_at_value))

        task = Task(
            title=request.POST['title'],
            due_at=due_at,
            priority=request.POST.get('priority', 'medium'),
        )
        task.save()

    if request.GET.get('order') == 'due':
        tasks = Task.objects.order_by('due_at')
    else:
        tasks = Task.objects.order_by('-posted_at')

    context = {
        'tasks': tasks
    }

    return render(request, 'todo/index.html', context)


def detail(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    context = {
        'task': task,
    }
    return render(request, 'todo/detail.html', context)


def delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.delete()
        return redirect('index')

    context = {
        'task': task
    }
    return render(request, 'todo/remove.html', context)


def update(request, task_id):
    task = get_object_or_404(Task, pk=task_id)

    if request.method == 'POST':
        task.title = request.POST['title']
        due_at_value = request.POST.get('due_at')
        task.due_at = make_aware(parse_datetime(due_at_value)) if due_at_value else None
        task.priority = request.POST.get('priority', 'medium')
        task.save()
        return redirect('detail', task_id=task_id)

    context = {
        'task': task
    }
    return render(request, "todo/edit.html", context)


def close(request, task_id):
    try:
        task = Task.objects.get(pk=task_id)
    except Task.DoesNotExist:
        raise Http404("Task does not exist")

    task.completed = True
    task.save()

    return redirect(index)