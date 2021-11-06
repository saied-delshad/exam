from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from core.utils import generate_random_string
from questions.models import QuestionModel

from exam_sessions.models import AbstractExamSession, CourseExamSession, SubjectExamSession, ExamResults


@receiver(pre_save, sender=CourseExamSession)
def add_ref_to_session(sender, instance, *args, **kwargs):
    """
    This function creates a unique reference number for Course Exam Sessions.
    The reference number starts with course_ses_ and continues with a code.
    """
    if instance and not instance.session_ref_number:
        ref_code = generate_random_string()
        instance.session_ref_number = "course_ses_" + ref_code


@receiver(pre_save, sender=SubjectExamSession)
def add_ref_to_session(sender, instance, *args, **kwargs):
    """
    This function creates a unique reference number for Subject Exam Sessions.
    The reference number starts with sub_ses_ and continues with a code.
    """
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
        noq = instance.subject_exam.noq_total
        questions = instance.subject_exam.subject.sub_questions.order_by('?')[:noq]
        instance.questions.add(*questions)


@receiver(pre_save, sender=ExamResults)
def has_exam_finished(sender, instance, *args, **kwargs):
    if instance.is_finished and not instance.score:
        session = instance.get_session()
        questions = session.questions.all()
        answers = instance.answers
        correctly_answered_questions = []
        for question in session.questions.all():
            question.numb_of_appeared = question.numb_of_appeared + 1 
            ref = question.question_ref_code
            if question.correct_answer-1 == answers.get(ref, None):
                correctly_answered_questions.append(ref)
                question.correctly_answered_times = question.correctly_answered_times + 1
            question.save()
        score = 100*len(correctly_answered_questions)/questions.count()
        instance.score = score
        ## to be used for checking pass/fail
    
    if not instance.pk and instance.session_ref_number:
        if instance.session_ref_number.startswith('sub'):
            exam = SubjectExamSession.objects.get(session_ref_number = instance.session_ref_number)
        elif instance.session_ref_number.startswith('course'):
            exam = CourseExamSession.objects.get(session_ref_number = instance.session_ref_number)
        if exam.show_score:
            instance.show_score = True





