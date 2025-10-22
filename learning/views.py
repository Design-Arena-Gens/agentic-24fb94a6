from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Q
from .models import GlossaryTerm, Lesson, Exercise, UserProgress
from .forms import GlossaryTermForm


def dashboard(request):
    """Main dashboard view"""
    total_lessons = Lesson.objects.filter(is_published=True).count()
    total_vocabulary = GlossaryTerm.objects.count()

    # Get user progress (demo user id=1)
    user_progress = UserProgress.objects.filter(user_id=1).select_related('lesson')
    completed_lessons = user_progress.filter(completed=True).count()
    in_progress_lessons = user_progress.filter(completed=False)[:5]

    recent_lessons = Lesson.objects.filter(is_published=True).order_by('-created_at')[:6]

    context = {
        'total_lessons': total_lessons,
        'completed_lessons': completed_lessons,
        'total_vocabulary': total_vocabulary,
        'in_progress_lessons': in_progress_lessons,
        'recent_lessons': recent_lessons,
        'completion_percentage': round((completed_lessons / total_lessons * 100) if total_lessons > 0 else 0, 2)
    }
    return render(request, 'learning/dashboard.html', context)


def glossary_list(request):
    """List all glossary terms with search and filtering"""
    terms = GlossaryTerm.objects.all()

    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        terms = terms.filter(
            Q(guarani_word__icontains=search_query) |
            Q(spanish_translation__icontains=search_query) |
            Q(english_translation__icontains=search_query)
        )

    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        terms = terms.filter(difficulty_level=difficulty)

    # Filter by category
    category = request.GET.get('category', '')
    if category:
        terms = terms.filter(category__icontains=category)

    # Get unique categories for filter dropdown
    categories = GlossaryTerm.objects.values_list('category', flat=True).distinct()

    context = {
        'terms': terms,
        'search_query': search_query,
        'selected_difficulty': difficulty,
        'selected_category': category,
        'categories': [c for c in categories if c],
    }
    return render(request, 'learning/glossary_list.html', context)


def glossary_detail(request, pk):
    """View single glossary term"""
    term = get_object_or_404(GlossaryTerm, pk=pk)
    return render(request, 'learning/glossary_detail.html', {'term': term})


def glossary_create(request):
    """Create new glossary term"""
    if request.method == 'POST':
        form = GlossaryTermForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Glossary term created successfully!')
            return redirect('learning:glossary-list')
    else:
        form = GlossaryTermForm()

    return render(request, 'learning/glossary_form.html', {'form': form, 'action': 'Create'})


def glossary_edit(request, pk):
    """Edit existing glossary term"""
    term = get_object_or_404(GlossaryTerm, pk=pk)

    if request.method == 'POST':
        form = GlossaryTermForm(request.POST, request.FILES, instance=term)
        if form.is_valid():
            form.save()
            messages.success(request, 'Glossary term updated successfully!')
            return redirect('learning:glossary-detail', pk=pk)
    else:
        form = GlossaryTermForm(instance=term)

    return render(request, 'learning/glossary_form.html', {'form': form, 'action': 'Edit', 'term': term})


def glossary_delete(request, pk):
    """Delete glossary term"""
    term = get_object_or_404(GlossaryTerm, pk=pk)

    if request.method == 'POST':
        term.delete()
        messages.success(request, 'Glossary term deleted successfully!')
        return redirect('learning:glossary-list')

    return render(request, 'learning/glossary_confirm_delete.html', {'term': term})


def lessons_list(request):
    """List all available lessons"""
    lessons = Lesson.objects.filter(is_published=True)

    # Filter by difficulty
    difficulty = request.GET.get('difficulty', '')
    if difficulty:
        lessons = lessons.filter(difficulty_level=difficulty)

    context = {
        'lessons': lessons,
        'selected_difficulty': difficulty,
    }
    return render(request, 'learning/lessons_list.html', context)


def lesson_detail(request, pk):
    """View lesson with content and exercises"""
    lesson = get_object_or_404(Lesson, pk=pk, is_published=True)
    content_blocks = lesson.content_blocks.all()
    exercises = lesson.exercises.all()

    # Track progress (demo user id=1)
    progress, created = UserProgress.objects.get_or_create(
        user_id=1,
        lesson=lesson
    )

    context = {
        'lesson': lesson,
        'content_blocks': content_blocks,
        'exercises': exercises,
        'progress': progress,
    }
    return render(request, 'learning/lesson_detail.html', context)


def exercise_view(request, pk):
    """View exercise with questions"""
    exercise = get_object_or_404(Exercise, pk=pk)
    questions = exercise.questions.prefetch_related('choices').all()

    context = {
        'exercise': exercise,
        'questions': questions,
    }
    return render(request, 'learning/exercise.html', context)
