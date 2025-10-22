from django import forms
from .models import GlossaryTerm


class GlossaryTermForm(forms.ModelForm):
    class Meta:
        model = GlossaryTerm
        fields = [
            'guarani_word', 'spanish_translation', 'english_translation',
            'pronunciation', 'audio_file', 'example_sentence_guarani',
            'example_sentence_spanish', 'category', 'difficulty_level'
        ]
        widgets = {
            'guarani_word': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Guarani word',
                'aria-label': 'Guarani word'
            }),
            'spanish_translation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter Spanish translation',
                'aria-label': 'Spanish translation'
            }),
            'english_translation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter English translation (optional)',
                'aria-label': 'English translation'
            }),
            'pronunciation': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Enter pronunciation guide',
                'aria-label': 'Pronunciation'
            }),
            'example_sentence_guarani': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter example sentence in Guarani',
                'rows': 3,
                'aria-label': 'Example sentence in Guarani'
            }),
            'example_sentence_spanish': forms.Textarea(attrs={
                'class': 'form-textarea',
                'placeholder': 'Enter example sentence in Spanish',
                'rows': 3,
                'aria-label': 'Example sentence in Spanish'
            }),
            'category': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g., Greetings, Numbers, Animals',
                'aria-label': 'Category'
            }),
            'difficulty_level': forms.Select(attrs={
                'class': 'form-select',
                'aria-label': 'Difficulty level'
            }),
            'audio_file': forms.FileInput(attrs={
                'class': 'form-file',
                'accept': 'audio/*',
                'aria-label': 'Audio file'
            })
        }
