from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.conf import settings
import uuid

from .models import (
    GlossaryTerm, Lesson, UserProgress, Exercise, Question,
    ExerciseAttempt, ChatMessage
)
from .serializers import (
    GlossaryTermSerializer, LessonListSerializer, LessonDetailSerializer,
    UserProgressSerializer, ExerciseAttemptSerializer, ChatMessageSerializer
)


class GlossaryTermViewSet(viewsets.ModelViewSet):
    """
    CRUD operations for Glossary Terms with search and filtering
    """
    queryset = GlossaryTerm.objects.all()
    serializer_class = GlossaryTermSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['guarani_word', 'spanish_translation', 'english_translation', 'category']
    ordering_fields = ['guarani_word', 'created_at', 'difficulty_level']

    def get_queryset(self):
        queryset = GlossaryTerm.objects.all()

        # Filter by difficulty level
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        # Filter by category
        category = self.request.query_params.get('category', None)
        if category:
            queryset = queryset.filter(category__icontains=category)

        return queryset

    @action(detail=False, methods=['get'])
    def categories(self, request):
        """Get list of unique categories"""
        categories = GlossaryTerm.objects.values_list('category', flat=True).distinct()
        return Response({'categories': [c for c in categories if c]})


class LessonViewSet(viewsets.ReadOnlyModelViewSet):
    """
    View lessons with detailed content and exercises
    """
    queryset = Lesson.objects.filter(is_published=True)
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return LessonDetailSerializer
        return LessonListSerializer

    def get_queryset(self):
        queryset = Lesson.objects.filter(is_published=True)

        # Filter by difficulty
        difficulty = self.request.query_params.get('difficulty', None)
        if difficulty:
            queryset = queryset.filter(difficulty_level=difficulty)

        return queryset


class UserProgressViewSet(viewsets.ModelViewSet):
    """
    Track and manage user progress through lessons
    """
    serializer_class = UserProgressSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        # In production, filter by request.user
        # For demo purposes, return all
        return UserProgress.objects.all()

    @action(detail=False, methods=['post'])
    def start_lesson(self, request):
        """Mark a lesson as started"""
        lesson_id = request.data.get('lesson_id')
        if not lesson_id:
            return Response({'error': 'lesson_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            lesson = Lesson.objects.get(id=lesson_id)
            # In production: user=request.user
            progress, created = UserProgress.objects.get_or_create(
                user_id=1,  # Demo user
                lesson=lesson
            )
            serializer = self.get_serializer(progress)
            return Response(serializer.data)
        except Lesson.DoesNotExist:
            return Response({'error': 'Lesson not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def complete_lesson(self, request):
        """Mark a lesson as completed"""
        lesson_id = request.data.get('lesson_id')
        score = request.data.get('score', 0)
        total_points = request.data.get('total_points', 0)

        if not lesson_id:
            return Response({'error': 'lesson_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            progress = UserProgress.objects.get(user_id=1, lesson_id=lesson_id)
            progress.completed = True
            progress.completion_date = timezone.now()
            progress.score = score
            progress.total_points = total_points
            progress.save()

            serializer = self.get_serializer(progress)
            return Response(serializer.data)
        except UserProgress.DoesNotExist:
            return Response({'error': 'Progress record not found'}, status=status.HTTP_404_NOT_FOUND)


class SubmitExerciseView(APIView):
    """
    Submit answers for exercise questions and get immediate feedback
    """
    permission_classes = [AllowAny]

    def post(self, request, exercise_id):
        try:
            exercise = Exercise.objects.get(id=exercise_id)
            answers = request.data.get('answers', [])

            results = []
            total_points = 0
            earned_points = 0

            for answer_data in answers:
                question_id = answer_data.get('question_id')
                user_answer = answer_data.get('answer', '')

                try:
                    question = Question.objects.get(id=question_id, exercise=exercise)
                    is_correct = user_answer.strip().lower() == question.correct_answer.strip().lower()
                    points = question.points if is_correct else 0

                    # Save attempt
                    attempt = ExerciseAttempt.objects.create(
                        user_id=1,  # Demo user
                        exercise=exercise,
                        question=question,
                        user_answer=user_answer,
                        is_correct=is_correct,
                        points_earned=points
                    )

                    results.append({
                        'question_id': question_id,
                        'is_correct': is_correct,
                        'correct_answer': question.correct_answer,
                        'explanation': question.explanation,
                        'points_earned': points,
                        'max_points': question.points
                    })

                    total_points += question.points
                    earned_points += points

                except Question.DoesNotExist:
                    continue

            return Response({
                'results': results,
                'total_points': total_points,
                'earned_points': earned_points,
                'percentage': round((earned_points / total_points * 100) if total_points > 0 else 0, 2)
            })

        except Exercise.DoesNotExist:
            return Response({'error': 'Exercise not found'}, status=status.HTTP_404_NOT_FOUND)


class ChatBotView(APIView):
    """
    AI-powered chatbot for Guarani language practice
    """
    permission_classes = [AllowAny]

    def post(self, request):
        message = request.data.get('message', '')
        session_id = request.data.get('session_id', str(uuid.uuid4()))

        if not message:
            return Response({'error': 'Message is required'}, status=status.HTTP_400_BAD_REQUEST)

        # Save user message
        ChatMessage.objects.create(
            session_id=session_id,
            role='user',
            message=message
        )

        # Generate AI response
        try:
            assistant_response = self._generate_response(message, session_id)
        except Exception as e:
            assistant_response = "Mba'éichapa! I'm your Guarani teacher. How can I help you learn today?"

        # Save assistant message
        ChatMessage.objects.create(
            session_id=session_id,
            role='assistant',
            message=assistant_response
        )

        return Response({
            'session_id': session_id,
            'response': assistant_response
        })

    def _generate_response(self, message, session_id):
        """Generate AI response using OpenAI"""
        if not settings.OPENAI_API_KEY:
            return "Mba'éichapa! I'm your Guarani language teacher. I can help you practice Guarani, answer questions about grammar, vocabulary, and culture. What would you like to learn today?"

        try:
            from openai import OpenAI
            client = OpenAI(api_key=settings.OPENAI_API_KEY)

            # Get conversation history
            history = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')[:10]
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful and patient Guarani language teacher. You help students learn Guarani (the indigenous language of Paraguay) through conversation, grammar explanations, vocabulary practice, and cultural insights. Be encouraging, provide examples, and correct mistakes gently. You can respond in Spanish or English when needed, but encourage Guarani practice."
                }
            ]

            for msg in history:
                messages.append({
                    "role": msg.role,
                    "content": msg.message
                })

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=300,
                temperature=0.7
            )

            return response.choices[0].message.content
        except Exception as e:
            return "Mba'éichapa! I'm here to help you learn Guarani. Ask me anything about the language, grammar, vocabulary, or culture!"


class ChatHistoryView(APIView):
    """
    Retrieve chat conversation history
    """
    permission_classes = [AllowAny]

    def get(self, request, session_id):
        messages = ChatMessage.objects.filter(session_id=session_id).order_by('created_at')
        serializer = ChatMessageSerializer(messages, many=True)
        return Response(serializer.data)


class DashboardStatsView(APIView):
    """
    Get dashboard statistics for user progress
    """
    permission_classes = [AllowAny]

    def get(self, request):
        # In production: filter by request.user
        user_id = 1  # Demo user

        # Total lessons and completed
        total_lessons = Lesson.objects.filter(is_published=True).count()
        completed_lessons = UserProgress.objects.filter(user_id=user_id, completed=True).count()

        # Total vocabulary terms
        total_vocabulary = GlossaryTerm.objects.count()

        # Recent progress
        recent_progress = UserProgress.objects.filter(user_id=user_id).order_by('-last_accessed')[:5]
        progress_serializer = UserProgressSerializer(recent_progress, many=True)

        # Exercises completed
        exercises_completed = ExerciseAttempt.objects.filter(user_id=user_id).values('exercise').distinct().count()

        # Average score
        avg_score = UserProgress.objects.filter(
            user_id=user_id,
            completed=True,
            total_points__gt=0
        ).aggregate(
            avg=Sum('score') * 100.0 / Sum('total_points')
        )['avg'] or 0

        return Response({
            'total_lessons': total_lessons,
            'completed_lessons': completed_lessons,
            'lessons_in_progress': UserProgress.objects.filter(user_id=user_id, completed=False).count(),
            'total_vocabulary': total_vocabulary,
            'exercises_completed': exercises_completed,
            'average_score': round(avg_score, 2),
            'recent_progress': progress_serializer.data,
            'completion_percentage': round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0, 2)
        })
