from django.db import models
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
import bcrypt
from datetime import datetime
# from apps.employees.models import Employee, How_well_known

# Create your models here.
class UserManager(models.Manager):
    def validate(self, form):
        errors = []
        try:
            user = self.get(email=form['email'])
            if not bcrypt.checkpw(form['password'].encode(), user.password.encode()):
                errors.append("Email or password is bad")
        except:
            errors.append('Email or password is bad')
        if len(errors)>0:
            return False
        else:
            return True

    def register_validate(self, form):
        errors = []
        if len(form['f_name'])<2:
            errors.append('First name is to short.')
        if len(form['l_name'])<2:
            errors.append('Last name is to short.')

        if not EMAIL_REGEX.match(form['email']):
            errors.append('Email must be valid')
        email_list = self.filter(email=form['email'])
        if len(email_list) > 0:
            errors.append('Email already in use')

        if len(form['password'])<2:
            errors.append('Password is to short.')
        if form['password'] != form['confirm_password']:
            errors.append('Password must match the Confirm password')
        return errors


    def create_user(self, form):
        pw_hash = bcrypt.hashpw(form['password'].encode(), bcrypt.gensalt())
        user = self.create(
            f_name=form['f_name'],
            l_name=form['l_name'],
            email=form['email'],
            password=pw_hash,
        )
        return user


class User(models.Model):
    f_name = models.CharField(max_length=255)
    l_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
        return "User: " + self.f_name

# class EmployeeManager(models.Manager):
#     def add_employee_verify(self, form):
#         errors = []
#         if len(form['fname'])<1:
#             errors.append('Must have a First Name')
#         if len(form['lname'])<1:
#             errors.append('Must have a Last Name')
#         if len(form['boss']) < 1:
#             errors.append('Must have a Supervisor name')
#         if len(form['jobtitle'])<1:
#             errors.append('Must have a Job Title')
#
#         return errors
#
#     def create_employee(self, form):
#         employee = self.create(
#             fname = form['fname'],
#             lname = form['lname'],
#             boss = form['boss'],
#             jobtitle = form['jobtitle'],
#             notes = form['notes'],
#             start_date = form['start_date'],
#             dob = form['dob'],
#             image = form['image'],
#         )
#         return employee
#
#
# class Employee(models.Model):
#     fname = models.CharField(max_length=255)
#     lname = models.CharField(max_length=255)
#     boss = models.CharField(max_length=500)
#     jobtitle = models.CharField(max_length=255)
#     rating = models.IntegerField(default=50)
#     image = models.ImageField(upload_to='profile_image', blank=True)
#     notes = models.TextField()
#     start_date = models.DateField(default=datetime.now)
#     dob = models.DateField(default=datetime.now)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
#     objects = EmployeeManager()
#
#
# class How_well_known(models.Model):
#     employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='how_well_known')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='how_well_known')
#     rating = models.IntegerField(default=50)
#     objects = EmployeeManager()