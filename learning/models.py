from django.db import models
from django.contrib.auth.models import User


class GlossaryTerm(models.Model):
    """Model for Guarani vocabulary terms"""
    guarani_word = models.CharField(max_length=200, db_index=True)
    spanish_translation = models.CharField(max_length=200)
    english_translation = models.CharField(max_length=200, blank=True)
    pronunciation = models.CharField(max_length=200, blank=True)
    audio_file = models.FileField(upload_to='audio/glossary/', blank=True, null=True)
    example_sentence_guarani = models.TextField(blank=True)
    example_sentence_spanish = models.TextField(blank=True)
    category = models.CharField(max_length=100, blank=True, db_index=True)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['guarani_word']
        verbose_name = 'Glossary Term'
        verbose_name_plural = 'Glossary Terms'

    def __str__(self):
        return f"{self.guarani_word} - {self.spanish_translation}"


class Lesson(models.Model):
    """Model for structured Guarani lessons"""
    title = models.CharField(max_length=200)
    description = models.TextField()
    order = models.IntegerField(default=0)
    difficulty_level = models.CharField(
        max_length=20,
        choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')],
        default='beginner'
    )
    cover_image = models.ImageField(upload_to='images/lessons/', blank=True, null=True)
    estimated_duration = models.IntegerField(help_text='Duration in minutes', default=15)
    is_published = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', 'title']

    def __str__(self):
        return self.title


class LessonContent(models.Model):
    """Model for lesson content blocks with multimedia support"""
    lesson = models.ForeignKey(Lesson, related_name='content_blocks', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)
    content_type = models.CharField(
        max_length=20,
        choices=[
            ('text', 'Text'),
            ('audio', 'Audio'),
            ('image', 'Image'),
            ('video', 'Video'),
            ('vocabulary', 'Vocabulary List')
        ],
        default='text'
    )
    title = models.CharField(max_length=200, blank=True)
    text_content = models.TextField(blank=True)
    audio_file = models.FileField(upload_to='audio/lessons/', blank=True, null=True)
    image_file = models.ImageField(upload_to='images/lessons/', blank=True, null=True)
    video_url = models.URLField(blank=True)
    vocabulary_terms = models.ManyToManyField(GlossaryTerm, blank=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.lesson.title} - Block {self.order}"


class Exercise(models.Model):
    """Model for exercises within lessons"""
    lesson = models.ForeignKey(Lesson, related_name='exercises', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.lesson.title} - {self.title}"


class Question(models.Model):
    """Model for individual questions within exercises"""
    exercise = models.ForeignKey(Exercise, related_name='questions', on_delete=models.CASCADE)
    question_type = models.CharField(
        max_length=20,
        choices=[
            ('multiple_choice', 'Multiple Choice'),
            ('fill_blank', 'Fill in the Blank'),
            ('true_false', 'True/False'),
            ('matching', 'Matching')
        ],
        default='multiple_choice'
    )
    question_text = models.TextField()
    audio_file = models.FileField(upload_to='audio/questions/', blank=True, null=True)
    image_file = models.ImageField(upload_to='images/questions/', blank=True, null=True)
    correct_answer = models.CharField(max_length=500)
    explanation = models.TextField(blank=True, help_text='Explanation shown after answering')
    points = models.IntegerField(default=10)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.exercise.title} - Q{self.order}"


class AnswerChoice(models.Model):
    """Model for multiple choice answer options"""
    question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=500)
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.choice_text


class UserProgress(models.Model):
    """Model to track user progress through lessons"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completion_date = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    total_points = models.IntegerField(default=0)
    started_at = models.DateTimeField(auto_now_add=True)
    last_accessed = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = 'User Progress'
        verbose_name_plural = 'User Progress Records'

    def __str__(self):
        return f"{self.user.username} - {self.lesson.title}"


class ExerciseAttempt(models.Model):
    """Model to track individual exercise attempts"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_answer = models.CharField(max_length=500)
    is_correct = models.BooleanField(default=False)
    points_earned = models.IntegerField(default=0)
    attempted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-attempted_at']

    def __str__(self):
        return f"{self.user.username} - {self.question}"


class ChatMessage(models.Model):
    """Model to store chatbot conversation history"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_id = models.CharField(max_length=100, db_index=True)
    role = models.CharField(
        max_length=20,
        choices=[('user', 'User'), ('assistant', 'Assistant'), ('system', 'System')],
        default='user'
    )
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.message[:50]}"
