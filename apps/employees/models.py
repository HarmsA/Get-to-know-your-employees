from django.db import models
from apps.users.models import User
from datetime import datetime
from pyuploadcare.dj.models import ImageField
from django.db.models.signals import post_delete, pre_delete
from quiz.settings import BASE_DIR
from django.dispatch import receiver
import os


# Create your models here.
class EmployeeManager(models.Manager):
    def add_employee_verify(self, form):
        errors = []
        if len(form['fname'])<1:
            errors.append('Must have a First Name')
        if len(form['lname'])<1:
            errors.append('Must have a Last Name')
        # if len(form['boss']) < 1:
        #     errors.append('Must have a Supervisor name')
        # if len(form['jobtitle'])<1:
        #     errors.append('Must have a Job Title')

        return errors

    def create_employee(self, form):
        employee = self.create(
            fname = form['fname'].strip().capitalize(),
            preferred_fname = form['pname'].strip().capitalize(),
            lname = form['lname'].strip().capitalize(),
            # boss = form['boss'].capitalize(),
            # jobtitle = form['jobtitle'],
            # notes = form['notes'],
            # start_date = form['start_date'],
            # dob = form['dob'],
        )
        return employee

    def verify_quiz(self, form):
        errors = []
        fname = form['fname'].strip().capitalize()
        pname = form['pname'].strip().capitalize()
        lname = form['lname'].strip().capitalize()
        employee = Employee.objects.get(id=form['id'])
        if fname != employee.fname:
            errors.append(f'First name is {employee.fname}')

        if employee.preferred_fname:
            if pname != employee.preferred_fname:
                errors.append(f'Perferred first name is {employee.preferred_fname}')
        elif pname and not employee.preferred_fname:
            errors.append("Employee uses first name and not a preferred name.")

        if lname != employee.lname:
            errors.append(f'Last name is {employee.lname}')
        return errors, employee

    def verify_update(self, form):
        errors = []
        if len(form['fname'])<1:
            errors.append('Must have a First Name')
        if len(form['lname'])<1:
            errors.append('Must have a Last Name')
        # if errors:
        return errors
        # else:
        #     fname = form['fname'].strip().capitalize()
        #     pname = form['pname'].strip().capitalize()
        #     lname = form['lname'].strip().capitalize()
        #     employee = Employee.objects.get(id=form['id'])
        #     employee = self.save(
        #         fname = fname,
        #         preferred_fname = pname,
        #         lname = lname
        #     )


class Employee(models.Model):
    fname = models.CharField(max_length=255)
    preferred_fname = models.CharField(max_length=100, blank=True)
    lname = models.CharField(max_length=255)
    boss = models.CharField(max_length=500)
    jobtitle = models.CharField(max_length=255)
    rating = models.IntegerField(default=50)
    notes = models.TextField()
    start_date = models.DateField(default=datetime.now)
    dob = models.DateField(default=datetime.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = EmployeeManager()

    def __str__(self):
        return "Employee: " + self.fname


class EmployeeImageManager(models.Manager):
    def verify_image(self, image):
        if image:
            return True
        return False

    def save_image(self, employee_image, employee_id):
        employee = Employee.objects.get(id=employee_id)
        image = self.create(
            employee=employee,
            image=employee_image,
        )
        return image



class Employee_Image(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='photo')
    image = models.ImageField(upload_to='media/', blank=True)
    title = models.CharField(max_length=255, default='Employee Photo')
    # image = ImageField(blank=True, manual_crop='')
    objects = EmployeeImageManager()


class How_well_known(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='how_well_known')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='how_well_known')
    rating = models.IntegerField(default=50)
    objects = EmployeeManager()