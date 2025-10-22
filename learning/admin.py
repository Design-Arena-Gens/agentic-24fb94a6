from django.contrib import admin
from .models import (
    GlossaryTerm, Lesson, LessonContent, Exercise, Question,
    AnswerChoice, UserProgress, ExerciseAttempt, ChatMessage
)


@admin.register(GlossaryTerm)
class GlossaryTermAdmin(admin.ModelAdmin):
    list_display = ['guarani_word', 'spanish_translation', 'category', 'difficulty_level', 'created_at']
    list_filter = ['difficulty_level', 'category']
    search_fields = ['guarani_word', 'spanish_translation', 'english_translation']


class LessonContentInline(admin.TabularInline):
    model = LessonContent
    extra = 1


class ExerciseInline(admin.TabularInline):
    model = Exercise
    extra = 1


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'difficulty_level', 'order', 'is_published', 'created_at']
    list_filter = ['difficulty_level', 'is_published']
    search_fields = ['title', 'description']
    inlines = [LessonContentInline, ExerciseInline]


@admin.register(LessonContent)
class LessonContentAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'content_type', 'title', 'order']
    list_filter = ['content_type']


class AnswerChoiceInline(admin.TabularInline):
    model = AnswerChoice
    extra = 4


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ['title', 'lesson', 'order']
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['exercise', 'question_type', 'question_text', 'order']
    list_filter = ['question_type']
    inlines = [AnswerChoiceInline]


@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ['user', 'lesson', 'completed', 'score', 'last_accessed']
    list_filter = ['completed']


@admin.register(ExerciseAttempt)
class ExerciseAttemptAdmin(admin.ModelAdmin):
    list_display = ['user', 'exercise', 'question', 'is_correct', 'points_earned', 'attempted_at']
    list_filter = ['is_correct']


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'role', 'message', 'created_at']
    list_filter = ['role']
