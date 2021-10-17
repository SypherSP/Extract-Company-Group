from django.urls import path, include
from . import views

app_name = "findgroup"

urlpatterns = [
    path('', views.index, name="index")
]

