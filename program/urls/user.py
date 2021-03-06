"""pysat URL Configuration for Program.User
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
from utils.permission import ActionType
from program.views import user

urlpatterns = [
    path('submit', view_maker(user.submit, 'POST', [
        ParamType.ProgramName,
        ParamType.ProgramCode,
        ParamType.ProgramDoc,
        ParamType.SchoolId,
        ParamType.ThemeId
    ], action=ActionType.UserAction)),

    path('like', view_maker(user.like, 'POST', [
        ParamType.ProgramId
    ], action=ActionType.UserLike)),

    path('download', view_maker(user.download, 'GET', [
        ParamType.ProgramId
    ], action=ActionType.UserAction))
]
