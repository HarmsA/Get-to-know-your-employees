from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from django.core import serializers
from .models import Employee, Employee_Image, How_well_known
from apps.users.models import User


from numpy import cumsum, sort, sum, searchsorted
from numpy.random import rand

# Create your views here.
def home(request):
    if 'user_id' not in request.session:
       return redirect('/login')
    users = User.objects.all()
    employee = Employee.objects.all()
    context = {
        'title': 'Dashboard',
        'employee':employee,
        'users':users,
    }
    return render(request, 'users/home.html', context)

def add_employee(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    context = {
        'title': 'Add Employee',
    }
    return render(request, 'employees/add_employee.html', context)

def verify_create_employee(request):
    errors = Employee.objects.add_employee_verify(request.POST)
    if errors:
        for error in errors:
            messages.error(request, error)
    else:
        employee = Employee.objects.create_employee(request.POST)
        employees = Employee.objects.all()
        image = request.FILES['employee_image']
        fs = FileSystemStorage()
        filename = fs.save(image.name, image)
        uploaded_file_url = fs.url(filename)
        file_save = Employee_Image.objects.save_image(uploaded_file_url, employee.id)
        # context={
        #     'employees':employees,
        #     'title': 'Employee list',
        #     'uploaded_file_url':uploaded_file_url,
        # }
        return redirect('/employees/view_employees')

    return render(request, 'employees/add_employee.html')

def view_employees(request):
    if 'user_id' not in request.session:
        return redirect('/login')
    employee = Employee.objects.all()
    fs = FileSystemStorage()
    uploaded_file_url = fs.url(employee)
    context = {
        'title': 'View Employees',
        'employees':employee,
        'uploaded_file_url': uploaded_file_url,

    }
    return render(request, 'employees/employee_list.html', context)


def quiz(request):
    if 'user_id' not in request.session:
       return redirect('/login')
    employees = Employee.objects.all().order_by('rating').reverse()
    weights = []
    n_picks = len(employees)

    for employee in employees:
        weights.append(employee.rating)
    t = cumsum(weights)
    s = sum(weights)
    weighted_employee = searchsorted(t,rand(n_picks)*s)
    w = weighted_employee[0]

    context = {
        'title': "Employee Quiz",
        'employee': employees[int(w)],
    }
    return render(request, 'employees/quiz.html', context)


def verify_quiz_entry(request):
    if request.method=='POST':
        errors, employee = Employee.objects.verify_quiz(request.POST)

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            error = 'Great Job! You know your employee.'
            messages.error(request, error)
        if len(errors)==3:
            employee.rating += 1
            encurage = f'Lets try again shortly.'
        if len(errors)==2:
            # employee.rating += 2
            encurage = 'Keep trying, your getting there.'
        if len(errors)==1:
            # employee.rating += 1
            encurage = 'Almost had it.'
        if len(errors) == 0:
            encurage = 'Great job, you know your employee.'
            if employee.rating > 5:
                employee.rating -= 5
            elif employee.rating<=5:
                employee.rating = 1
        employee.save()
        print('employee rating ', employee.rating)
        context = {
            'employee': employee,
            'encurage': encurage,
        }
        return render(request, 'employees/quiz_answer.html', context)

    return redirect('employees:home')

def quiz_answer(request):
    return redirect('/employees/quiz')

def update(request, employee_id):
    employee = Employee.objects.get(id=employee_id)
    context = {
        'title': 'Update Employee',
        'employee': employee
    }
    return render(request, 'employees/update.html', context)

def verify_update_employee(request):
    if request.method=='POST':
        errors = Employee.objects.verify_update(request.POST)
    else:
        return redirect('/employees/view_employees')
    if errors:
        for error in errors:
            messages.error(request, error)
        employee = Employee.objects.get(id=request.POST['id'])
        context = {
            'title': 'Update Employee',
            'employee': employee
        }
        return render(request, 'employees/update.html', context)
    else:
        employee = Employee.objects.get(id=request.POST['id'])
        employee.fname = request.POST['fname'].strip().capitalize()
        employee.preferred_fname = request.POST['pname'].strip().capitalize()
        employee.lname = request.POST['lname'].strip().capitalize()
        employee.save()
    try:
        if request.FILES['employee_image']:
            print(request.FILES['employee_image'])
            image = request.FILES['employee_image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            uploaded_file_url = fs.url(filename)
            employee.photo.delete()
            file_save = Employee_Image.objects.save_image(uploaded_file_url, employee.id)
    except KeyError:
        print("No image updated")
    return redirect('/employees/view_employees')



def delete(request, employee_id):
    Employee.objects.get(id=employee_id).delete()
    return redirect('/employees/view_employees')