from django.urls import path,include
from .views import simple_upload,async_uploader

urlpatterns = [

    path('',simple_upload,name='simple_upload'),
    path('async/',async_uploader,name='async_file_upload'),

]
