
from django import forms
from django.http.response import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth import login,logout,authenticate
from django.db import IntegrityError
from .forms import TaskForm,AuthenticationForm,CustomUserCreationForm,UserUpdateForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required # para proteger las rutas
from django.contrib.auth import views as auth_views

from django.utils import timezone
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.views import View
from .mixins import UserIsAdminMixin
from .models import User
from tasks import forms

# Create your views here.



class HomePageView(TemplateView):
    template_name = 'tasks/home.html'

# def home(request):
#     return render(request, "tasks/home.html")

class UserListView(LoginRequiredMixin,UserIsAdminMixin,ListView):
    template_name = 'tasks/list_user.html'
    model = User


class UserUpdateView(LoginRequiredMixin,UserIsAdminMixin,UpdateView):
    template_name = 'tasks/update_user.html'
    model = User
    form_class = UserUpdateForm
    pk_url_kwarg = 'user_id'
    success_url = reverse_lazy('web:user:list')



class UserCreateView(LoginRequiredMixin,UserIsAdminMixin,CreateView):
    template_name = 'tasks/signup.html'
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('web:home')

    def form_valid(self, form: CustomUserCreationForm) -> HttpResponse:
        user: User = form.instance
        user.set_password(form.cleaned_data['password'])
        return super().form_valid(form)
    



# signup
# def UserCreateView(request):
#     if request.method == "GET":
#         return render(request, "tasks/signup.html", {"form": CustomUserCreationForm})
#     else:
#         if request.POST["password1"] == request.POST["password2"]:
#             try:
#                 user = User.objects.create_user(
#                     username=request.POST["username"],
#                     password=request.POST["password1"],
#                 )
#                 user.save()
#                 login(request, user) # con esto se guarda la sesion del usuario que se acaba de registrar
#                 return redirect("tasks")
#             except IntegrityError:

#                 return render(
#                     request,
#                     "tasks/signup.html",
#                     {"form": CustomUserCreationForm, "error": "User already exists"},
#                 )

#         return render(
#             request,
#             "tasks/signup.html",
#             {"form": CustomUserCreationForm, "error": "Passwords do not match"},
#         )


class TaskPendingListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user,datecompleted__isnull=True)
# @login_required
# def tasks(request):
#     tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
#     return render(request, "tasks/tasks.html", {'tasks':tasks})




class TaskCompletedListView(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'tasks/tasks.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user,datecompleted__isnull=False)
# @login_required
# def tasks_completed(request):
#     tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False)
#     return render(request,'tasks/tasks.html',{'tasks':tasks})



class TaskCreateView(LoginRequiredMixin,CreateView):
    model = Task
    template_name = 'tasks/create_task.html'
    form_class = TaskForm
    login_url = 'web:signin'
    success_url = reverse_lazy('web:tasks:tasks_pending')

    def form_valid(self, form): # Es para asignar el usuario
        form.instance.user = self.request.user
        return super().form_valid(form)
    

# @login_required
# def create_task(request):
#     if request.method == 'GET':
#         return render(request,'tasks/create_task.html',{'form':TaskForm})
        
#     else:
#         try:
#             form = TaskForm(request.POST)
#             new_task = form.save(commit=False)
#             new_task.user = request.user
#             new_task.save()
#             return redirect('tasks')
#         except ValueError:
#             return render(request,'tasks/create_task.html',{'form':TaskForm,'error':'Please enter valid data'})


class TaskUpdateView(LoginRequiredMixin,UpdateView): # Uso UpdateView porque en el detalle de la vista Fazt configro para que se pueda actualizar
    model = Task
    template_name = 'tasks/task_detail.html'
    form_class = TaskForm
    login_url = 'tasks:signin'
    context_object_name = 'task'
    success_url = reverse_lazy('web:tasks:tasks_pending')

    def get_queryset(self): # con esto me aseguro qwue se puedan actualizar solo las tareas del usuario logueado
        return Task.objects.filter(user=self.request.user)



# @login_required
# def task_detail(request,task_id): # para actualizar los datos que ingresé en el formulario (mediante el formulario creado TaskForm)
#     if request.method == 'GET':
#         task = get_object_or_404(Task, pk=task_id, user=request.user)
#         form = TaskForm(instance=task)
#         return render(request,'tasks/task_detail.html', {'task':task,'form':form})
#     else:
#         try:
#             task = get_object_or_404(Task, pk=task_id,user=request.user)
#             form = TaskForm(request.POST,instance=task) # con el instance=task le estoy diciendo que use al usuario de la instancia de task, si no pongo, tendria que asignar el usuario manualmnente como en la funcion create_task. Y con request.POST le estoy diciendo que me traiga los nuevos datos ingresados
#             form.save()
#             return redirect('tasks')
#         except ValueError:
#             return render(request,'tasks/task_detail.html', {'task':task,'form':form,'error':'Error updating task'})


class TaskCompleteView(LoginRequiredMixin, UpdateView):
    model = Task
    fields = []  # No necesitas un formulario, ya que no se editan campos desde el formulario
    login_url = 'tasks:signin'
    success_url = reverse_lazy('web:tasks:tasks_pending')

    def form_valid(self, form):
        task = form.save(commit=False)
        task.datecompleted = timezone.now()  # Actualizamos el campo 'datecompleted'
        task.save()
        return redirect(self.success_url)

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    



# @login_required
# def complete_task(request,task_id): # para actualizar el campo datecomplete
#     task = get_object_or_404(Task,pk=task_id)
#     task.datecompleted = timezone.now()
#     task.save()
#     return redirect('tasks:tasks_pending')


class TaskDeleteView(LoginRequiredMixin,DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('web:tasks:tasks_pending')
    login_url = 'tasks:signin'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

# @login_required
# def delete_task(request,task_id):
#     task = get_object_or_404(Task,pk=task_id)
#     task.delete()
#     return redirect('tasks:tasks_pending')



class LogoutView(LoginRequiredMixin,View):
    def post(self,request):
        return auth_views.logout_then_login(request,login_url=reverse_lazy('web:signin'))
# @login_required
# def signout(request):
#     logout(request) # con esto se cierra sesion
#     return redirect('tasks:home')



class LoginView(auth_views.LoginView):
    authentication_form = AuthenticationForm  # Formulario personalizado
    template_name = 'tasks/signin.html'  # Plantilla que renderizará el formulario
    redirect_authenticated_user = True  # Redirige al usuario si ya está autenticado
    next_page = reverse_lazy('web:home')  # URL a la que redirigir después de un login exitoso (opcional)




class PasswordChangeView(LoginRequiredMixin,auth_views.PasswordChangeView):
    template_name = 'tasks/password-change.html'
    success_url = reverse_lazy('web:home')
    

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