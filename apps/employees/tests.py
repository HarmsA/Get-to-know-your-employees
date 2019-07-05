from django.test import TestCase
from .models import Employee
from django.utils import timezone
import time

class EmployeeTest(TestCase):
    def test_employee_creations(self):
        employee = Employee.objects.create(
            fname='Adam',
            preferred_fname='Harms',
            lname='Harms',
            # boss = form['boss'].capitalize(),
            # jobtitle = form['jobtitle'],
            # notes = form['notes'],
            # start_date = form['start_date'],
            # dob = form['dob'],
        )
        t=2
        time.sleep(t)
        now = timezone.now()
        self.assertLess(employee.created_at, now)


