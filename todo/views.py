from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import  User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import ToDo
from django.contrib.auth.decorators import login_required

def home(request):
    return render(request, 'todo/home.html')

def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {"form": CustomUserCreationForm()})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect("currenttodos")
            except IntegrityError:
                return render(request, 'todo/signupuser.html',
                              {"form": CustomUserCreationForm(), "error": "That username has already been taken. Create a new one"})
        else:
            return render(request, 'todo/signupuser.html', {"form": CustomUserCreationForm(), "error": "Passwords didn't match"})

def loginuser(request):
    if request.method == "GET":
        return render(request, 'todo/loginuser.html', {"form": CustomAuthenticationForm()})
    else:
        username = request.POST["username"]
        password = request.POST["password"]
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return render(request, "todo/loginuser.html",
                          {"form": CustomAuthenticationForm(), "error":"User does not exist"})
        else:
            user = authenticate(request, username=username, password=password)

        if user is None:
            return render(request, 'todo/loginuser.html',
                          {'form': CustomAuthenticationForm(), 'error':'Username and password didn\'t match'})
        else:
            login(request, user)
            return redirect('currenttodos')

@login_required
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

@login_required
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'todo/createtodo.html', {"form": TodoForm()})
    else:
        try:
            form = TodoForm(request.POST)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in.'})

@login_required
def currenttodos(request):
    todos = ToDo.objects.filter(user=request.user, done=False).order_by('deadline_datetime')
    return render(request, 'todo/currenttodos.html', {'todos': todos})

@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, done=True).order_by('deadline_datetime')
    return render(request, 'todo/completedtodos.html', {'todos': todos})

@login_required
def viewtodo(request, todo_pk):
    todo_task = get_object_or_404(ToDo, pk=todo_pk, user=request.user)

    if request.method == 'GET':
        form = TodoForm(instance=todo_task)
        return render(request, 'todo/viewtodo.html', {'todo_task': todo_task, 'form': form})
    else:
        try:
            form = TodoForm(request.POST, instance=todo_task)
            form.save()
            return redirect('currenttodos')
        except ValueError:
            return render(request, 'todo/viewtodo.html', {'todo_task': todo_task, 'form': form, 'error': 'Bad Info'})

@login_required
def completetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.done = True
        todo.save()
        return redirect('currenttodos')

@login_required
def deletetodo(request, todo_pk):
    todo = get_object_or_404(ToDo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todo.delete()
        return redirect('currenttodos')
