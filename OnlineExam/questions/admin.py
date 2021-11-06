from django.contrib import admin
from questions.models import CourseModel, SubjectModel, QuestionModel, CourseExamModel,\
                             SubjectExamModel, PerSubjectModel
from import_export.admin import ImportExportModelAdmin
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError

@admin.register(CourseModel)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'created_at']

@admin.register(SubjectModel)
class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'created_at', 'course']

@admin.register(QuestionModel)
class QuestionModelAdmin(ImportExportModelAdmin):
    list_display = ['question_ref_code', 'created_at','difficulty_level', 'subject' ]
    list_filter = ['difficulty_level', 'subject']
    search_fields = ['question_ref_code', 'subject__subject_name', 'question_content']
    readonly_fields = ['numb_of_appeared', 'correctly_answered_times', 'created_by']

    def save_model(self, request, obj, form, change):
        instance = form.save(commit=False)
        if not getattr(instance, 'created_by', None):
            instance.created_by = request.user
        return super(QuestionModelAdmin, self).save_model(request, obj, form, change)



class SubjectInlineFormSet(BaseInlineFormSet):
    def clean(self):
        super(SubjectInlineFormSet, self).clean()
        total = 0
        for form in self.forms:
            if form.cleaned_data and form.cleaned_data.get('noq_subject'):
                total += form.cleaned_data['noq_subject']
        if self.instance.noq_total != total:
            difference = self.instance.noq_total - total
            if difference > 0:
                raise ValidationError('Total number of questions per subject is %s less\
                   than total number of questions defined for the exam' %str(difference))
            elif difference < 0:
                raise ValidationError('Total number of questions per subject is %s more\
                   than total number of questions defined for the exam' %str(difference))




class AddSubjectQInline(admin.StackedInline):
    """
    This class adds fields to determine number of questions related to each subject in the course
    """
    model = PerSubjectModel
    formset = SubjectInlineFormSet
    extra = 0

    def has_add_permission(self, request, obj=None):
        return False
    
    def has_delete_permission(self, request, obj=None):
        return False
    


@admin.register(CourseExamModel)
class CourseExamModelAdmin(admin.ModelAdmin):

    inlines = [AddSubjectQInline]

    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):

        context.update({
            'show_save': False,
            'show_save_and_add_another': False,
        })
        return super().render_change_form(request, context, add, change, form_url, obj)


admin.site.register(SubjectExamModel)