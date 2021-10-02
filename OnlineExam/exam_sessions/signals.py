from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.utils import generate_random_string

from exam_sessions.models import AbstractExamSession, CourseExamSession, SubjectExamSession


@receiver(pre_save, sender=CourseExamSession)
def add_ref_to_question(sender, instance, *args, **kwargs):
    if instance and not instance.session_ref_number:
        ref_code = generate_random_string()
        instance.session_ref_number = "course_ses_" + ref_code


@receiver(pre_save, sender=SubjectExamSession)
def add_ref_to_question(sender, instance, *args, **kwargs):
    if instance and not instance.session_ref_number:
        ref_code = generate_random_string()
        instance.session_ref_number = "sub_ses_" + ref_code


@receiver(post_save, sender=CourseExamSession)
def select_questions(sender, instance, created, **kwargs):
    exam_subjects = instance.course_exam.course.subjects.all()
    per_subject_exam = instance.course_exam.exam_for_course.all()
    instance.questions.clear()
    if instance.pk:
        for exam_subject in exam_subjects:
            noq = per_subject_exam.get(subject=exam_subject).noq_subject
            questions = exam_subject.sub_questions.order_by('?')[:noq]
            instance.questions.add(*questions)
