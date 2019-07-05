from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
from apps.employees.models import Employee


# ======== login/register pages ==================================
def login(request):
    context = {
        'title': 'Login',
    }
    return render(request, 'users/login.html', context)

def process_login(request):
    print(request.POST)
    if User.objects.validate(request.POST):
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
    else:
        error = 'Email or password is incorrect, please verify or register.'
        messages.error(request, error)
        return redirect('/login')
    return redirect('/home')

def process_register(request):
    errors = User.objects.register_validate(request.POST)

    if errors:
        for error in errors:
            messages.error(request, error)
    else:
        user =User.objects.create_user(request.POST)
        print(user.f_name)
        request.session['user_id'] = user.id
        return redirect('/home')
    return redirect('/login')


# ============= View job/Dasboard pages==========================================

def home(request):
   # if 'user_id' not in request.session:
   #     return redirect('/login')
   # name = User.objects.get(id=request.session['user_id'])
    users = User.objects.all()
    employee = Employee.objects.all()
    context = {
       # 'name':name,
        'title': 'Dashboard',
        'employee':employee,
        'users':users,
    }

    return render(request, 'users/home.html', context)


def logout(request):
    request.session.clear()
    return redirect('/login')
