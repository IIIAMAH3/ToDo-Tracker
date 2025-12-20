from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm, CustomUserCreationForm, CustomAuthenticationForm
from .models import ToDo
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def home(request):
    return render(request, 'todo/home.html')


def signupuser(request):
    if request.method == "GET":
        return render(request, 'todo/signupuser.html', {"form": CustomUserCreationForm()})
    else:
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():

            user = form.save()
            login(request, user)

            return redirect("currenttodos")

        else:
            first_error = None
            for errors in form.errors.values():
                if errors:
                    first_error = errors[0]
                    break

            return render(request, "todo/signupuser.html", {
                "form": form,
                "error": first_error,
            })

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
            if form.is_valid():
                newtodo = form.save(commit=False)
                newtodo.user = request.user
                newtodo.save()
                return redirect('currenttodos')
            else:
                return render(request, "todo/createtodo.html", {"form": form})
        except ValueError:
            return render(request, 'todo/createtodo.html', {'form': TodoForm(), 'error': 'Bad data passed in.'})


@login_required
def currenttodos(request):
    todos = ToDo.objects.filter(user=request.user, done=False).order_by('-deadline_datetime')

    paginator = Paginator(todos, 4)
    page = request.GET.get("page", 1)

    try:
        todos = paginator.page(page)
    except PageNotAnInteger:
        todos = paginator.page(1)
    except EmptyPage:
        todos = paginator.page(paginator.num_pages)

    return render(request, 'todo/currenttodos.html', {'todos': todos})


@login_required
def completedtodos(request):
    todos = ToDo.objects.filter(user=request.user, done=True).order_by('-deadline_datetime')

    paginator = Paginator(todos, 4)
    page = request.GET.get("page", 1)

    try:
        todos = paginator.page(page)
    except PageNotAnInteger:
        todos = paginator.page(1)
    except EmptyPage:
        todos = paginator.page(paginator.num_pages)
        
    return render(request, 'todo/completedtodos.html', {'todos': todos})


@login_required
def viewtodo(request, todo_pk):
    todo_task = get_object_or_404(ToDo, pk=todo_pk, user=request.user)

    next_page = request.GET.get("next", "currenttodos")

    if request.method == 'GET':
        form = TodoForm(instance=todo_task)
        return render(request, 'todo/viewtodo.html', {
            'todo_task': todo_task,
            'form': form,
            'next_page': next_page,
        })
    else:
        form = TodoForm(request.POST, instance=todo_task)

        next_page = request.POST.get("next", "currenttodos")

        if form.is_valid():
            form.save()

            return redirect(next_page)

        else:
            first_error = None
            for errors in form.errors.values():
                if errors:
                    first_error = errors[0]
                    break

            return render(request, 'todo/viewtodo.html', {
                'todo_task': todo_task,
                'form': form,
                'error': first_error,
                'next_page': next_page
            })


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


def custom_404_view(request, exception):
    """
    Custom 404 error handler that maintains site header and footer

    Args:
        request: HttpRequest object
        exception: The exception that triggered the 404

    Returns:
        HttpResponse with 404 status and full site layout
    """
    context = {
        "exception": str(exception),
        "path": request.path,
    }

    return render(request, template_name="404.html", context=context, status=404)
