'''
Registration file for django-modeltranslation.
'''
from modeltranslation.translator import register, TranslationOptions
from .models import Question, Category, Survey, Answer

@register(Survey)
class SurveyTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(Category)
class CategoryTranslationOptions(TranslationOptions):
    fields = ('name', 'description',)


@register(Question)
class QuestionTranslationOptions(TranslationOptions):
    fields = ('text', 'choices')


@register(Answer)
class AnswerTranslationOptions(TranslationOptions):
    fields = ('body',)
