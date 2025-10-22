from django.urls import path
from . import views

app_name = 'learning'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('glossary/', views.glossary_list, name='glossary-list'),
    path('glossary/create/', views.glossary_create, name='glossary-create'),
    path('glossary/<int:pk>/', views.glossary_detail, name='glossary-detail'),
    path('glossary/<int:pk>/edit/', views.glossary_edit, name='glossary-edit'),
    path('glossary/<int:pk>/delete/', views.glossary_delete, name='glossary-delete'),
    path('lessons/', views.lessons_list, name='lessons-list'),
    path('lessons/<int:pk>/', views.lesson_detail, name='lesson-detail'),
    path('exercises/<int:pk>/', views.exercise_view, name='exercise-view'),
]
