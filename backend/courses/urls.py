from django.urls import path
from .views import *

urlpatterns = [
    # ### Course List API's
    path('get_courses_list', get_courses_list, name='get_courses_list'),
    path('get_course_modules', get_course_modules, name='get_course_modules'),

    path('get_module_detail', get_module_detail, name='get_module_detail'),

    # student register/unregister module apis
    path('get_student_module_register', get_student_module_register, name='get_student_module_register'),
    path('add_student_module_register', student_module_register, name='add_student_module_register'),
    path('student_module_unregister', student_module_unregister, name='student_module_unregister'),
]