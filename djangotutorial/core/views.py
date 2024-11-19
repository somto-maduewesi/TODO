from django.shortcuts import render, redirect
from django.http.response import HttpResponse, JsonResponse
from django.http import HttpRequest
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Todo
from django.contrib.auth.models import User

# Create your views here.
def home_page(request):
    # always take in a request
    return render(request, 'index.html')

def login_view(request: HttpRequest):
    if request.method == "POST":
        user = authenticate(
            request, 
            username = request.POST['username'], 
            password = request.POST['password']
            )
        print(user)
        if user: #if User Exists
            #Log User In
            login(request, user = user)
            #Redirect To Todo
            return redirect('/todo/')
        else:
            #Incorrect details
            messages.error(request, 'Invalid Login Details')
    return render(request, 'login.html')

def logout_view(request: HttpRequest):
    logout(request)
    return redirect('/')

def signup_view(request: HttpRequest):
    if request.method == "POST":
        if request.POST['password'] != request.POST['confirm']:
            messages.error(request, "Passwords Do Not Match!")
            return render(request, 'signup.html')
        if len(request.POST['password']) <= 5:
            messages.error(request, "Password Must Be At Leats 6 Characters")
            return render(request, 'signup.html')
        
        new_user = User.objects.create(
            username = request.POST['username'],
            email = request.POST['email']
        )
        new_user.set_password(request.POST['password'])
        new_user.save()
        
        user = authenticate(
            request, 
            username = request.POST['username'], 
            password = request.POST['password']
            )
        print(user)
        if user: #if User Exists
            #Log User In
            login(request, user = user)
            #Redirect To Todo
            return redirect('/todo/')
        else:
            #Incorrect details
            messages.error(request, 'Invalid Login Details')
    return render(request, 'signup.html')

def todo_view(request: HttpRequest):
    if request.user.is_authenticated:
        if request.method == "POST": 
            newTodo = Todo.objects.create(
                user = request.user,
                todo = request.POST['task']
            )
            return redirect('/todo')
        my_todos = Todo.objects.filter(user = request.user)
        data = {
            'data': my_todos
        }
        return render(request, 'todo.html', data)
    else:
        return redirect('/login/')
    
def delete_todo_view(request, id):
    todo = Todo.objects.get(id = id)
    todo.delete()
    return redirect('/todo')

def toggle_completed_view(request, id):
    todo = Todo.objects.get(id = id)
    todo.done = not todo.done
    todo.save()
    return redirect('/todo')