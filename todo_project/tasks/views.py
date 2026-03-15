from django.shortcuts import render, redirect
from .models import Task
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import TaskSerializer


def register(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')

    return render(request, 'tasks/register.html', {'form': form})


@login_required
def task_list(request):
    search = request.GET.get('search')

    tasks = Task.objects.filter(user=request.user)

    if search:
        tasks = tasks.filter(title__icontains=search)

    return render(request, 'tasks/task_list.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'POST':
        title = request.POST.get('title')

        if title and title.strip():
            Task.objects.create(
                title=title.strip(),
                user=request.user
            )

    return redirect('task_list')


@login_required
def edit_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)

    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.save()
        return redirect('task_list')

    return render(request, 'tasks/edit_task.html', {'task': task})


@login_required
def delete_task(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.delete()
    return redirect('task_list')


@login_required
def toggle_complete(request, pk):
    task = Task.objects.get(id=pk, user=request.user)
    task.completed = not task.completed
    task.save()
    return redirect('task_list')


@api_view(['GET'])
def task_api(request):
    tasks = Task.objects.all()
    serializer = TaskSerializer(tasks, many=True)
    return Response(serializer.data)
@api_view(['GET', 'POST'])
def tasks_api(request):

    if request.method == 'GET':

        tasks = Task.objects.filter(user=request.user)
        serializer = TaskSerializer(tasks, many=True)

        return Response(serializer.data)

    if request.method == 'POST':

        serializer = TaskSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response(serializer.data)

        return Response(serializer.errors)
@api_view(['GET', 'PUT', 'DELETE'])
def task_detail_api(request, pk):

        task = Task.objects.get(id=pk, user=request.user)

        if request.method == 'GET':
            serializer = TaskSerializer(task)
            return Response(serializer.data)

        elif request.method == 'PUT':
            serializer = TaskSerializer(task, data=request.data)

            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)

            return Response(serializer.errors)

        elif request.method == 'DELETE':
            task.delete()
            return Response({"message": "Task deleted"})