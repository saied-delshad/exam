from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.utils import generate_random_string

from questions.models import QuestionModel, CourseExamModel, PerSubjectModel

@receiver(pre_save, sender=QuestionModel)
def add_ref_creator_to_question(sender, instance, *args, **kwargs):
    if instance and not instance.question_ref_code:
        ref_code = generate_random_string()
        instance.question_ref_code = ref_code



@receiver(post_save, sender=CourseExamModel)
def add_subjects(sender, instance, created, **kwargs):
    if created:
        for subject in instance.course.subjects.all():
            PerSubjectModel.objects.create(course_exam=instance, subject=subject)

    elif instance.tracker.has_changed('course'):
        for exam_subject in instance.exam_for_course.all():
            exam_subject.delete()
        for subject in instance.course.subjects.all():
            PerSubjectModel.objects.create(course_exam=instance, subject=subject)
