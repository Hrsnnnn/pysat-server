"""pysat URL Configuration for School.admin
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType

from school.views import admin

urlpatterns = [
    path('approve', view_maker(admin.approve, 'POST', [
        ParamType.ApplyId,
        ParamType.Approve
    ])),
    path('applylist', view_maker(admin.get_apply_list, 'POST', [
        ParamType.SchoolId,
        ParamType.ApplyListType,
        ParamType.Page
    ]))
]
