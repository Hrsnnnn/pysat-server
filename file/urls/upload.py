"""pysat URL Configuration for File Upload
"""
from django.urls import path

from utils.views import view_maker
from utils.params import ParamType
import file.views.upload as views

urlpatterns = [
    path('test', view_maker(views.test, 'POST')),
    path('start', view_maker(views.start, 'POST', [
        ParamType.SchoolId,
        ParamType.CategoryId,
        ParamType.Filename,
        ParamType.VideoTitle,
        ParamType.Description
    ])),
    path('chunk', views.chunk),
    path('done', view_maker(views.done, 'POST', [
        ParamType.FileKey
    ]))
]
