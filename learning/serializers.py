from rest_framework import serializers
from .models import (
    GlossaryTerm, Lesson, LessonContent, Exercise, Question,
    AnswerChoice, UserProgress, ExerciseAttempt, ChatMessage
)


class GlossaryTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = '__all__'


class AnswerChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnswerChoice
        fields = ['id', 'choice_text', 'order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = AnswerChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'question_type', 'question_text', 'audio_file',
            'image_file', 'correct_answer', 'explanation', 'points',
            'order', 'choices'
        ]


class ExerciseSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Exercise
        fields = ['id', 'title', 'instructions', 'order', 'questions']


class LessonContentSerializer(serializers.ModelSerializer):
    vocabulary_terms = GlossaryTermSerializer(many=True, read_only=True)

    class Meta:
        model = LessonContent
        fields = [
            'id', 'order', 'content_type', 'title', 'text_content',
            'audio_file', 'image_file', 'video_url', 'vocabulary_terms'
        ]


class LessonDetailSerializer(serializers.ModelSerializer):
    content_blocks = LessonContentSerializer(many=True, read_only=True)
    exercises = ExerciseSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = [
            'id', 'title', 'description', 'difficulty_level',
            'cover_image', 'estimated_duration', 'content_blocks', 'exercises'
        ]


class LessonListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title', 'description', 'difficulty_level', 'cover_image', 'estimated_duration', 'order']


class UserProgressSerializer(serializers.ModelSerializer):
    lesson_title = serializers.CharField(source='lesson.title', read_only=True)

    class Meta:
        model = UserProgress
        fields = [
            'id', 'lesson', 'lesson_title', 'completed', 'completion_date',
            'score', 'total_points', 'started_at', 'last_accessed'
        ]


class ExerciseAttemptSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExerciseAttempt
        fields = ['id', 'exercise', 'question', 'user_answer', 'is_correct', 'points_earned', 'attempted_at']


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        fields = ['id', 'session_id', 'role', 'message', 'created_at']
