from django.conf.urls import url
from . import views

app_name = 'employees'

urlpatterns = [
    url(r'^$',views.home, name='home'),
    url(r'^add_employee/$', views.add_employee, name='add_employee'),
    # url(r'^update_employee/$',views.update_employee, name='update_employee'),
    url(r'^verify_create_employee/$', views.verify_create_employee, name='verify_create_employee'),
    url(r'^add_employee/verify_create_employee/$', views.verify_create_employee, name='verify_create_employee'),
    url(r'^view_employees/$', views.view_employees, name='view_employees'),
    url(r'^quiz/$', views.quiz, name='quiz'),
    url(r'^verify_quiz_entry/$', views.verify_quiz_entry, name='verify_quiz_entry'),
    url(r'^quiz_answer/$', views.quiz_answer, name='quiz_answer'),
    url(r'^delete/(?P<employee_id>\d+)/$',views.delete, name='delete'),
]