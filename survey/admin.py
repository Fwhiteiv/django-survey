from django.conf import settings
from django.contrib import admin

from survey.actions import make_published
from survey.exporter.csv import Survey2Csv
from survey.exporter.tex import Survey2Tex
from survey.models import Answer, Category, Question, Response, Survey


class QuestionInline(admin.StackedInline):
    model = Question
    ordering = ("order", "category")
    extra = 1

    def get_formset(self, request, survey_obj, *args, **kwargs):
        formset = super().get_formset(request, survey_obj, *args, **kwargs)
        if survey_obj:
            formset.form.base_fields["category"].queryset = survey_obj.categories.all()
        return formset


class CategoryInline(admin.TabularInline):
    model = Category
    extra = 0


class SurveyAdmin(admin.ModelAdmin):
    list_display = ("name", "is_published", "need_logged_user", "template")
    list_filter = ("is_published", "need_logged_user")
    inlines = [CategoryInline, QuestionInline]
    actions = [make_published, Survey2Csv.export_as_csv, Survey2Tex.export_as_tex]


class AnswerBaseInline(admin.StackedInline):
    fields = ("question", "body")
    readonly_fields = ("question",)
    extra = 0
    model = Answer


class ResponseAdmin(admin.ModelAdmin):
    list_display = ("interview_uuid", "survey", "created", "user")
    list_filter = ("survey", "created")
    date_hierarchy = "created"
    inlines = [AnswerBaseInline]
    # specifies the order as well as which fields to act on
    readonly_fields = ("survey", "created", "updated", "interview_uuid", "user")


if 'modeltranslation' in settings.INSTALLED_APPS:
    from modeltranslation.admin import TabbedTranslationAdmin, TranslationStackedInline, TranslationTabularInline

    class TranslationQuestionInline(QuestionInline, TranslationStackedInline):
        pass


    class TranslationCategoryInline(CategoryInline, TranslationTabularInline):
        pass


    class TranslationAnswerInline(AnswerBaseInline, TranslationStackedInline):
        pass


    class TranslationResponseAdmin(ResponseAdmin):
        # Directly apply media, because Response is not a translation registered model
        class Media:
                js = (
                    'http://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js',
                    'http://ajax.googleapis.com/ajax/libs/jqueryui/1.10.2/jquery-ui.min.js',
                    'modeltranslation/js/tabbed_translation_fields.js',
                )
                css = {
                    'screen': ('modeltranslation/css/tabbed_translation_fields.css',),
                }

        inlines = [TranslationAnswerInline]


    class TranslationSurveyAdmin(SurveyAdmin, TabbedTranslationAdmin):
        inlines = [TranslationCategoryInline, TranslationQuestionInline]


    admin.site.register(Survey, TranslationSurveyAdmin)
    admin.site.register(Response, TranslationResponseAdmin)
else:
    admin.site.register(Survey, SurveyAdmin)
    admin.site.register(Response, ResponseAdmin)

# admin.site.register(Question, QuestionInline)
# admin.site.register(Category, CategoryInline)
