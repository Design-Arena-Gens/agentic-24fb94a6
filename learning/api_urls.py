from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'glossary', api_views.GlossaryTermViewSet, basename='glossary')
router.register(r'lessons', api_views.LessonViewSet, basename='lesson')
router.register(r'progress', api_views.UserProgressViewSet, basename='progress')

urlpatterns = [
    path('', include(router.urls)),
    path('chat/', api_views.ChatBotView.as_view(), name='chatbot'),
    path('chat/history/<str:session_id>/', api_views.ChatHistoryView.as_view(), name='chat-history'),
    path('exercises/<int:exercise_id>/submit/', api_views.SubmitExerciseView.as_view(), name='submit-exercise'),
    path('dashboard/', api_views.DashboardStatsView.as_view(), name='dashboard'),
]
