"""pysat URL Configuration for School.Create
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType

from school.views import user

urlpatterns = [
    path('apply', view_maker(user.apply_for_school, 'POST', [
        ParamType.ApplyMessage,
        ParamType.SchoolName
    ], [
        ParamType.ApplyMessage,
        ParamType.SchoolName
    ], action=ActionType.ApplyForSchool))
]
