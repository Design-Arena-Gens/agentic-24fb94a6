import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'guarani_app.settings')
django.setup()

from django.contrib.auth.models import User
from learning.models import GlossaryTerm, Lesson, LessonContent, Exercise, Question, AnswerChoice

# Create demo user
user, _ = User.objects.get_or_create(username='demo', defaults={'email': 'demo@example.com'})
user.set_password('demo')
user.save()

# Create some glossary terms
glossary_data = [
    {
        'guarani_word': 'Mba\'éichapa',
        'spanish_translation': '¿Cómo estás?',
        'english_translation': 'How are you?',
        'pronunciation': 'mbah-eh-ee-CHA-pa',
        'category': 'Greetings',
        'difficulty_level': 'beginner',
        'example_sentence_guarani': 'Mba\'éichapa, mitã?',
        'example_sentence_spanish': '¿Cómo estás, amigo?'
    },
    {
        'guarani_word': 'Aguyje',
        'spanish_translation': 'Gracias',
        'english_translation': 'Thank you',
        'pronunciation': 'ah-goo-YEH',
        'category': 'Greetings',
        'difficulty_level': 'beginner',
        'example_sentence_guarani': 'Aguyje nde pytyvõ rehe',
        'example_sentence_spanish': 'Gracias por tu ayuda'
    },
    {
        'guarani_word': 'Ñanduti',
        'spanish_translation': 'Tela de araña / Internet',
        'english_translation': 'Spider web / Internet',
        'pronunciation': 'nyan-doo-TEE',
        'category': 'Technology',
        'difficulty_level': 'intermediate',
        'example_sentence_guarani': 'Aheka mba\'e ñandutípe',
        'example_sentence_spanish': 'Busco cosas en internet'
    },
    {
        'guarani_word': 'Mburuvicha',
        'spanish_translation': 'Líder, jefe',
        'english_translation': 'Leader, chief',
        'pronunciation': 'mboo-roo-VEE-cha',
        'category': 'Social',
        'difficulty_level': 'intermediate',
    },
    {
        'guarani_word': 'Ñe\'ẽ',
        'spanish_translation': 'Palabra, lenguaje',
        'english_translation': 'Word, language',
        'pronunciation': 'nye-EH',
        'category': 'Language',
        'difficulty_level': 'beginner',
    }
]

for term_data in glossary_data:
    GlossaryTerm.objects.get_or_create(
        guarani_word=term_data['guarani_word'],
        defaults=term_data
    )

# Create lessons
lesson1, _ = Lesson.objects.get_or_create(
    title='Introduction to Guarani Greetings',
    defaults={
        'description': 'Learn basic greetings and expressions in Guarani. Master the essential phrases for everyday conversation.',
        'difficulty_level': 'beginner',
        'estimated_duration': 15,
        'order': 1,
        'is_published': True
    }
)

lesson2, _ = Lesson.objects.get_or_create(
    title='Numbers and Counting',
    defaults={
        'description': 'Learn how to count and use numbers in Guarani. Essential for daily life and shopping.',
        'difficulty_level': 'beginner',
        'estimated_duration': 20,
        'order': 2,
        'is_published': True
    }
)

lesson3, _ = Lesson.objects.get_or_create(
    title='Family and Relationships',
    defaults={
        'description': 'Vocabulary for family members and describing relationships in Guarani culture.',
        'difficulty_level': 'intermediate',
        'estimated_duration': 25,
        'order': 3,
        'is_published': True
    }
)

# Add content to lesson 1
LessonContent.objects.get_or_create(
    lesson=lesson1,
    order=1,
    defaults={
        'content_type': 'text',
        'title': 'Welcome to Guarani!',
        'text_content': '''Guarani is an indigenous language spoken by millions of people in Paraguay, where it is an official language alongside Spanish. It is one of the few indigenous languages in the Americas with such widespread use.

In this lesson, you will learn the most common greetings and how to introduce yourself in Guarani.'''
    }
)

LessonContent.objects.get_or_create(
    lesson=lesson1,
    order=2,
    defaults={
        'content_type': 'text',
        'title': 'Basic Greetings',
        'text_content': '''Here are the essential greetings you need to know:

• Mba'éichapa - How are you? (informal)
• Aguyje - Thank you
• Porãite - I'm fine
• Maitei - Hello (formal)'''
    }
)

# Create exercise for lesson 1
exercise1, _ = Exercise.objects.get_or_create(
    lesson=lesson1,
    title='Greetings Practice',
    defaults={
        'instructions': 'Test your knowledge of Guarani greetings!',
        'order': 1
    }
)

# Add questions
q1, created = Question.objects.get_or_create(
    exercise=exercise1,
    order=1,
    defaults={
        'question_type': 'multiple_choice',
        'question_text': 'How do you say "How are you?" in Guarani?',
        'correct_answer': 'Mba\'éichapa',
        'explanation': 'Mba\'éichapa is the most common informal greeting in Guarani.',
        'points': 10
    }
)

if created:
    AnswerChoice.objects.create(question=q1, choice_text='Mba\'éichapa', order=1)
    AnswerChoice.objects.create(question=q1, choice_text='Aguyje', order=2)
    AnswerChoice.objects.create(question=q1, choice_text='Maitei', order=3)
    AnswerChoice.objects.create(question=q1, choice_text='Porãite', order=4)

q2, created = Question.objects.get_or_create(
    exercise=exercise1,
    order=2,
    defaults={
        'question_type': 'multiple_choice',
        'question_text': 'What does "Aguyje" mean?',
        'correct_answer': 'Thank you',
        'explanation': 'Aguyje is used to express gratitude in Guarani.',
        'points': 10
    }
)

if created:
    AnswerChoice.objects.create(question=q2, choice_text='Hello', order=1)
    AnswerChoice.objects.create(question=q2, choice_text='Thank you', order=2)
    AnswerChoice.objects.create(question=q2, choice_text='Goodbye', order=3)
    AnswerChoice.objects.create(question=q2, choice_text='Please', order=4)

q3, created = Question.objects.get_or_create(
    exercise=exercise1,
    order=3,
    defaults={
        'question_type': 'fill_blank',
        'question_text': 'Complete the greeting: "_____, mitã?" (How are you, friend?)',
        'correct_answer': 'Mba\'éichapa',
        'explanation': 'The complete greeting is "Mba\'éichapa, mitã?"',
        'points': 15
    }
)

print("Demo data created successfully!")
print("- Created 5 glossary terms")
print("- Created 3 lessons")
print("- Created 1 exercise with 3 questions")
print("- Demo user: username='demo', password='demo'")
