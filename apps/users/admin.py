from django.contrib import admin
from apps.employees.models import Employee, Employee_Image, How_well_known
from apps.users.models import User
# Register your models here.
admin.site.register(User)
admin.site.register(Employee)
admin.site.register(Employee_Image)
admin.site.register(How_well_known)