from django.urls import path
from . import views

urlpatterns = [
    path('',views.ListGroup.as_view(), name="single"),
    path('create-group/', views.CreateGroup.as_view(), name="create-group")
]
