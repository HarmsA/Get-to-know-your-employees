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
        return redirect('/dashboard')
    return redirect('/login')

# ========= create/edit Jobs pages =============================================
#
# def add_employee(request):
#     # if 'user_id' not in request.session:
#     #     return redirect('/login')
#     context = {
#         'title': 'Add Employee',
#     }
#     return render(request, 'users/../employees/templates/employees/add_employee.html', context)
#
# def verify_create_employee(request):
#     print('8'*80)
#     print(type(request.POST['image']))
#     errors = Employee.objects.add_employee_verify(request.POST)
#     if errors:
#         for error in errors:
#             messages.error(request, error)
#     else:
#         employee = Employee.objects.create_employee(request.POST)
#         return redirect('/view_employees')
#     return redirect('/add_employee')

def create_job_for_user(request, job_id):
    job = Job.objects.get(id=job_id)
    user = User.objects.get(id=request.session['user_id'])
    job.worker = user
    job.save()
    return redirect('/dashboard')

def edit_job(request, job_id):
    job = Job.objects.get(id=job_id)
    context = {
        'title':'Edit Job',
        'job' : job
    }
    return render(request, 'users/edit_job.html', context)

def update_job_verify(request):
    errors = Job.objects.addjob_verify(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
        job = Job.objects.get(id=request.POST['id'])
        context = {
            'title': 'Edit Job',
            'job': job
        }
        return render(request, 'users/edit_job.html', context)
    else:
        job = Job.objects.get(id=request.POST['id'])
        job.title=request.POST['title']
        job.description=request.POST['description']
        job.location=request.POST['location']
        job.save()
    return redirect('/dashboard')

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

# def view_employees(request):
#     employee = Employee.objects.all()
#     context = {
#         'title': 'View Employees',
#         'employees':employee,
#     }
#     return render(request, 'users/../employees/templates/employees/employee_list.html', context)

# ============= logout, delete/cancel pages==========================================



def logout(request):
    request.session.clear()
    return redirect('/login')
