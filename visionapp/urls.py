from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('edit_description/<int:description_id>/', views.edit_description, name='edit_description'),
]
