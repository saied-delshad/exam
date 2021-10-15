from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.utils import generate_random_string

from exam_sessions.models import AbstractExamSession, CourseExamSession, SubjectExamSession


@receiver(pre_save, sender=CourseExamSession)
def add_ref_to_session(sender, instance, *args, **kwargs):
    if instance and not instance.session_ref_number:
        ref_code = generate_random_string()
        instance.session_ref_number = "course_ses_" + ref_code


@receiver(pre_save, sender=SubjectExamSession)
def add_ref_to_session(sender, instance, *args, **kwargs):
    if instance and not instance.session_ref_number:
        ref_code = generate_random_string()
        instance.session_ref_number = "sub_ses_" + ref_code


@receiver(post_save, sender=CourseExamSession)
def select_questions(sender, instance, created, **kwargs):
    """
    This function select questions randomly for each subject in the exam.
    Number of questions (noq) is determined for each subject in Course Exam Model.
    The questions are re-selected after each save.
    """
    exam_subjects = instance.course_exam.course.subjects.all()
    per_subject_exam = instance.course_exam.exam_for_course.all()
    instance.questions.clear()
    if instance.pk:
        for exam_subject in exam_subjects:
            noq = per_subject_exam.get(subject=exam_subject).noq_subject
            questions = exam_subject.sub_questions.order_by('?')[:noq]
            instance.questions.add(*questions)


@receiver(post_save, sender=SubjectExamSession)
def select_questions(sender, instance, created, **kwargs):
    """
    This function select questions randomly the exam.
    The number of questions (noq) is determined in Subject Exam Model.
    The questions are re-selected after each save.
    """
    instance.questions.clear()
    if instance.pk:
        noq = instance.subject.noq_total
        questions = instance.subject_exam.subject.sub_questions.order_by('?')[:noq]
        instance.questions.add(*questions)