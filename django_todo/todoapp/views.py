from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .forms import *
from .models import *


def LoginView(request):
    template_name = "account/login.html"

    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None and UserProfile.objects.filter(user=user).exists():
                login(request, user)
                return redirect("home") 
            else:
                error_message = "Invalid Username"
        else:
            error_message = "Invalid Username or Password"

        return render(request, template_name, {'form': form, 'error_message': error_message})

    else:
        form = LoginForm()
        return render(request, template_name, {'form': form})



def UserRegisterView(request):
    template_name = "account/register.html"
    
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            username = request.POST.get("username")
            password = request.POST.get("password")
            email = request.POST.get("email")

            if User.objects.filter(username=username).exists():
                error = "Sorry! User with this username already exists."
                return render(request, template_name, {'form': form, 'error': error})

            if User.objects.filter(email=email).exists():
                error1 = "Sorry! User with this email already exists. Please try a new email."
                return render(request, template_name, {'form': form, 'error1': error1})

            user = User.objects.create_user(username, email, password)
            user_profile = UserProfile.objects.create(
                user=user, 
                name=request.POST.get('name'), 
                address=request.POST.get('address'), 
                phone=request.POST.get('phone'), 
                email=email
            )
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, template_name, {'form': form}) 


@login_required()
def Home(request):
    template_name = "dashboard/home.html"
    userprofile = UserProfile.objects.get(user=request.user)
    task = Task.objects.filter(created_by=userprofile) 
    completed = Task.objects.filter(created_by=userprofile, completed=True)
    incompleted = Task.objects.filter(created_by=userprofile, completed=False)
    total_incompleted_task = Task.objects.filter(completed=False, created_by=userprofile).count()
    context = {
        'task' : task,
        'completed' : completed,
        'incompleted' : incompleted,
        'total_incompleted_task' : total_incompleted_task
        
    }
    return render(request, template_name, context)

@login_required()
def TaskDetail(request, pk):
    template_name = "dashboard/detail.html"
    task = Task.objects.get(id=pk) 
    context = { 
        
        'task':task
    }
    return render(request, template_name, context)

@login_required()
def AddTask (request):
    template_name ='dashboard/addtask.html'
    userprofile = UserProfile.objects.get(user=request.user)
    form = TaskForm
    if request.method == 'POST':
        form = TaskForm(request.POST, request.FILES) 
        form.instance.created_by = userprofile
        if form.is_valid():
                form.save()
                return redirect('addtask')
    context = {
        'form' : form
        } 
    return render(request, template_name, context)

@login_required()
def EditTask(request,pk):
    template_name ='dashboard/edittask.html'
    task = Task.objects.get(id=pk)
    form = EditTaskForm
    if request.method == 'POST':
        form = EditTaskForm(request.POST, instance=task)
        if form.is_valid():
                form.save()
                return redirect('home')
        else:
            form =EditTaskForm(instance=task) 
    context = {
        'task' : task,
        'form' : form
    }
    return render(request, template_name,context)

@login_required()
def DeleteTask(request,pk):
    template_name ='dashboard/deletetask.html'
    task = Task.objects.get(id=pk)
    if request.method == 'POST':
     task.delete()
     return redirect('/')
    context ={
        'task' : task
    }
    return render(request, template_name,context)



   

