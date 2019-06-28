from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

from django.core.files.storage import FileSystemStorage
from django.core import serializers
from .models import Employee, Employee_Image, How_well_known
from apps.users.models import User
import pprint

import time

from numpy import cumsum, sort, sum, searchsorted
from numpy.random import rand

# Create your views here.
def home(request):
    if 'user_id' not in request.session:
       return redirect('/login')
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
        context={
            'employees':employees,
            'title': 'Employee list',
            'uploaded_file_url':uploaded_file_url,
        }
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
    # if 'quiz_rating' not in request.session:
    #     request.session['quiz_rating'] = 0
    # else:
    #     request.session['quiz_rating'] += 1

    employees = Employee.objects.all().order_by('rating').reverse()
    weights = []
    n_picks = len(employees)

    for employee in employees:
        weights.append(employee.rating)
    print(weights)
    t = cumsum(weights)
    s = sum(weights)
    weighted_employee = searchsorted(t,rand(n_picks)*s)
    print('len of employee', len(employees))
    # print(request.session['quiz_rating'])
    w = weighted_employee[0]
    # if len(employees) <= request.session['quiz_rating']:
    #     request.session['quiz_rating'] = 0
    context = {
        'title': "Employee Quiz",
        'employee': employees[int(w)],
        # 'employee': weighted_employee[0],
    }
    return render(request, 'employees/quiz.html', context)


def verify_quiz_entry(request):
    if request.method=='POST':
        print(request.POST['fname'])
        print(request.POST['pname'])
        print(request.POST['lname'])
        fname = request.POST['fname'].strip().capitalize()
        pname = request.POST['pname'].strip().capitalize()
        lname = request.POST['lname'].strip().capitalize()
        errors = []
        employee = Employee.objects.get(id=request.POST['id'])

        if fname != employee.fname:
            errors.append(f'First name is {employee.fname}')

        if employee.preferred_fname:
            if pname != employee.preferred_fname:
                errors.append(f'Perferred first name is {employee.preferred_fname}')

        if lname != employee.lname:
            errors.append(f'Last name is {employee.lname}')

        if errors:
            for error in errors:
                messages.error(request, error)
        else:
            error = 'Great Job! You know your employee.'
            # for error in errors:
            messages.error(request, error)
        if len(errors)==3:
            employee.rating += 3
            encurage = f'Lets try again shortly.'
        if len(errors)==2:
            employee.rating += 2
            encurage = 'Keep trying, your getting there.'
        if len(errors)==1:
            employee.rating += 1
            encurage = 'Almost had it.'
        if len(errors) == 0:
            encurage = 'Great job, you know your employee.'
            if employee.rating > 5:
                employee.rating -= 5
        employee.save()
        print('employee rating ', employee.rating)
        context = {
            'employee': employee,
            'encurage': encurage,
        }
        # return redirect('/employees/quiz')
        return render(request, 'employees/quiz_answer.html', context)

    return redirect('employees:home')

def quiz_answer(request):
    # if request.method == 'POST':
    #     employee = Employee.objects.get(id)
    # print(employee.fname)
    # employees_json = serializers.serialize('json', employee)
    # pp = pprint.PrettyPrinter(indent=4)
    # return render(request, 'employees/quiz_answer.html', {'employee':employee})
    return redirect('/employees/quiz')


def delete(request, employee_id):
    Employee.objects.get(id=employee_id).delete()
    return redirect('/employees/view_employees')