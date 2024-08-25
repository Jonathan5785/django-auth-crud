from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm,CustomUserCreationForm,CustomAuthenticationForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # para proteger las rutas
from django.contrib.auth.views import LoginView
# Create your views here.


def home(request):
    return render(request, "tasks/home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "tasks/signup.html", {"form": CustomUserCreationForm})
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user) # con esto se guarda la sesion del usuario que se acaba de registrar
                return redirect("tasks")
            except IntegrityError:

                return render(
                    request,
                    "tasks/signup.html",
                    {"form": CustomUserCreationForm, "error": "User already exists"},
                )

        return render(
            request,
            "tasks/signup.html",
            {"form": CustomUserCreationForm, "error": "Passwords do not match"},
        )

@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, "tasks/tasks.html", {'tasks':tasks})

@login_required
def tasks_completed(request):
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
    return render(request,'tasks/tasks.html',{'tasks':tasks})

@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request,'tasks/create_task.html',{'form':TaskForm})
        
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'tasks/create_task.html',{'form':TaskForm,'error':'Please enter valid data'})

@login_required
def task_detail(request,task_id): # para actualizar los datos que ingresé en el formulario (mediante el formulario creado TaskForm)
    if request.method == 'GET':
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request,'tasks/task_detail.html', {'task':task,'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id,user=request.user)
            form = TaskForm(request.POST,instance=task) # con el instance=task le estoy diciendo que use al usuario de la instancia de task, si no pongo, tendria que asignar el usuario manualmnente como en la funcion create_task. Y con request.POST le estoy diciendo que me traiga los nuevos datos ingresados
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request,'tasks/task_detail.html', {'task':task,'form':form,'error':'Error updating task'})

@login_required
def complete_task(request,task_id): # para actualizar el campo datecomplete
    task = get_object_or_404(Task,pk=task_id)
    task.datecompleted = timezone.now()
    task.save()
    return redirect('tasks')

@login_required
def delete_task(request,task_id):
    task = get_object_or_404(Task,pk=task_id)
    task.delete()
    return redirect('tasks')

@login_required
def signout(request):
    logout(request) # con esto se cierra sesion
    return redirect('home')

# def signin(request):
#     if request.method == 'GET':
#         return render(request,'tasks/signin.html',{'form':CustomAuthenticationForm})
#     else:
#         user = authenticate(
#             request,username=request.POST['username'],
#             password=request.POST['password']
#             ) # Con esto verifica si el usuario existe en la base de datos
#         if user is None:
#             return render(request,'tasks/signin.html',{'form':CustomAuthenticationForm,'error':'User does not exist'})
#         else:
#             login(request, user) # Con esto se guarda la sesion del usuario que se acaba de autenticar
#             return redirect('tasks')

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm  # Formulario personalizado
    template_name = 'tasks/signin.html'  # Plantilla que renderizará el formulario
    redirect_authenticated_user = True  # Redirige al usuario si ya está autenticado
    next_page = '/'  # URL a la que redirigir después de un login exitoso (opcional)

