from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import TodoForm
from .models import Todo


def get_showing_todos(req, todos):
    filter = req.GET.get("filter", "all")
    if filter == "completed":
        return todos.filter(is_completed=True)
    elif filter == "incompleted":
        return todos.filter(is_completed=False)
    else:
        return todos

@login_required
def index(req):
    todos = Todo.objects.filter(owner=req.user)
    completed_count = todos.filter(is_completed=True).count()
    incompleted_count = todos.filter(is_completed=False).count()
    all_count = todos.count()

    context = {"todos": get_showing_todos(req, todos), "all_count": all_count,
               "completed_count": completed_count,
               "incompleted_count": incompleted_count}

    return render(req, "todo/index.html", context)

@login_required
def create_todo(req):
    if req.method == "POST":
        title = req.POST.get("title")
        description = req.POST.get("description")
        is_completed = req.POST.get("is_completed", False)

        todo = Todo()

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.owner=req.user
        todo.save()
        
        messages.add_message(req, messages.SUCCESS,
                             "The todo was successfully added")

        return HttpResponseRedirect(reverse("todo", kwargs={'id': todo.pk}))

    elif req.method == "GET":
        form = TodoForm()
        context = {'form': form}
        return render(req, "todo/create-todo.html", context)

@login_required
def todo_detail(req, id):
    todo = get_object_or_404(Todo, pk=id)
    context = {"todo": todo}
    return render(req, "todo/todo-detail.html", context)

@login_required
def todo_delete(req, id):
    if req.method == "POST":
        todo = get_object_or_404(Todo, pk=id)
        todo.delete()
        messages.add_message(req, messages.SUCCESS,
                             "The todo was successfully deleted")
        return HttpResponseRedirect(reverse("home"))

@login_required
def todo_edit(req, id):
    todo = get_object_or_404(Todo, pk=id)
    if req.method == "GET":
        form = TodoForm(instance=todo)
        context = {"todo": todo, "form": form}
        return render(req, "todo/todo-edit.html", context)

    elif req.method == "POST":
        title = req.POST.get("title")
        description = req.POST.get("description")
        is_completed = req.POST.get("is_completed", False)

        todo.title = title
        todo.description = description
        todo.is_completed = True if is_completed == "on" else False
        todo.save()

        messages.add_message(req, messages.SUCCESS,
                             "The todo was successfully updated")

        return HttpResponseRedirect(reverse("home"))
