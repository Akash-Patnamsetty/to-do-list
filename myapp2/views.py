from django.shortcuts import render,redirect
from .models import Task
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
# Create your views here.
def registration(request):
    if request.method=="POST":
        username=request.POST.get("user")    
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        if username=="" or password1=="" or password2=="":
            if username=="":
                messages.error(request,"user name are not be null")
            else:
                messages.error(request,"passwords are not be null")
        elif username==password1:
            messages.error(request,"user name and password are not equal ")
        elif len(password1)<6:
            messages.error(request,"password must contain atleast 6 characters") 
        elif password1!=password2:
            messages.error(request," passwords are not match ") 
        else:
            if User.objects.filter(username=username).exists():
               messages.error(request,"username already taken")
               return redirect("registration")
            else:
                user=User.objects.create_user(username=username,password=password1)
                user.save()
                messages.success(request,"successfully create account")
                login(request,user)    
                return redirect("login_view")
    return render(request,"signin.html")

def login_view(requset):
    if requset.method=="POST":
        username=requset.POST.get("username")
        password=requset.POST.get("password")
        user=authenticate(username=username,password=password)
        if user:
            login(requset, user)
            return redirect("task_list")
        else:
            messages.error(requset,"user details  not available")
            messages.error(requset,"signup now") 
            return render(requset,"signin.html")
            
    return render(requset,"login.html")

def task_list(request):
    task=Task.objects.filter(User=request.user)
    return render(request,"main.html",{'task':task})

def add_task(request):
    if request.method=="POST":
        title=request.POST.get("title")
        task=request.POST.get("task")
        Task.objects.create(User=request.user,title=title,task=task)
        return  redirect("task_list")
    return render(request,"add_task.html") 

def delete_task(request,id):
    d=Task.objects.get(User=request.user,id=id)
    d.delete()
    return redirect("task_list")

def edit_task(request,id):
    if request.method=="POST":
        title=request.POST.get("title")
        task=request.POST.get("task")
        tk=Task.objects.get(User=request.user,id=id)
        tk.title=title
        tk.task=task
        tk.save()
        return  redirect("task_list")
    else:
        task=Task.objects.get(User=request.user,id=id)
        return render(request,"edit_task.html",{"task":task})

def exit_user(request):
    logout(request)
    return redirect("login_view")