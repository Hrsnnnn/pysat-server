"""pysat URL Configuration for School.Create
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from school.views import school

urlpatterns = [
    path('create', view_maker(school.create_school, 'POST', [
        ParamType.UsernameWithDefault,
        ParamType.SchoolName,
        ParamType.Description
    ], [
        ParamType.SchoolName
    ], action=ActionType.CreateSchool))
]
