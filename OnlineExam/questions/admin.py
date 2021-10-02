from django.contrib import admin
from questions.models import CourseModel, SubjectModel, QuestionModel, CourseExamModel, SubjectExamModel, PerSubjectModel

@admin.register(CourseModel)
class CourseModelAdmin(admin.ModelAdmin):
    list_display = ['course_name', 'created_at']

@admin.register(SubjectModel)
class SubjectModelAdmin(admin.ModelAdmin):
    list_display = ['subject_name', 'created_at', 'course']

@admin.register(QuestionModel)
class QuestionModelAdmin(admin.ModelAdmin):
    list_display = ['question_ref_code', 'created_at', 'last_update', 'difficulty_level', 'subject' ]

class AddSubjectQInline(admin.StackedInline):
    """
    This class adds fields to determine number of questions related to each subject in the course
    """
    model = PerSubjectModel
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