from django.db.models.signals import pre_save, post_save
import json
from django.dispatch import receiver
from core.utils import generate_random_string
from questions.models import QuestionModel
from exam_sessions.send_scores import send_score

from exam_sessions.models import CourseExamSession, SubjectExamSession, FreeExamSession, ExamResults


@receiver(pre_save, sender=CourseExamSession)
def add_ref_to_course_session(sender, instance, *args, **kwargs):
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


@receiver(pre_save, sender=FreeExamSession)
def add_ref_to_session_free(sender, instance, *args, **kwargs):
    """
    This function creates a unique reference number for Free Exam Sessions.
    The reference number starts with free_ses_ and continues with a code.
    """
    if instance and not instance.session_ref_number:
        ref_code = generate_random_string()
        instance.session_ref_number = "free_ses_" + ref_code



@receiver(post_save, sender=CourseExamSession)
def select_course_exam_questions(sender, instance, created, **kwargs):
    """
    This function select questions randomly for each subject in the exam.
    Number of questions (noq) is determined for each subject in Course Exam Model.
    The questions are re-selected after each save.
    """
    if ExamResults.objects.filter(session_ref_number = instance.session_ref_number).count() == 0:
        instance.questions.clear()
        exam_subjects = instance.course_exam.course.subjects.all()
        per_subject_exam = instance.course_exam.exam_for_course.all()
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
def set_timer(sender, instance, *args, **kwargs):
    if not instance.exam_duration:
        instance.exam_duration = instance.get_exam_time()
    if instance._state.adding:
        instance.exam_remaining = instance.exam_duration * 60


@receiver(pre_save, sender=ExamResults)
def has_exam_finished(sender, instance, *args, **kwargs):
    """
    This method calculates the score and save a snap shot of the exam taken for generating
    transcript.
    """
    if instance.is_finished and instance.score == None:
        session = instance.get_session()
        questions = session.questions.all()
        answers = instance.answers
        sorting = instance.snapshot
        if not sorting:
            sorting = re_sort(questions)
        if answers == None:
            answers = {}
        correctly_answered_questions = []
        not_answered = {}
        snap_shot = []
        instance.num_not_answered = 0
        wrong_answered = {}
        penalties = 0
        instance.num_wrong = 0
        for k, v in sorting.items():
            question = questions.get(question_ref_code = v)
            question.numb_of_appeared = question.numb_of_appeared + 1 
            answer = answers.get(v, None)
            if answer == None:
                not_answered.update({v:''})
                instance.num_not_answered += 1
            elif question.correct_answer-1 == answer:
                correctly_answered_questions.append(v)
                question.correctly_answered_times += 1
            else:
                instance.num_wrong +=1
                wrong_answered.update({v:answer})
            snap_shot.append({'ref':v, 'body': question.question_content, 'A':question.opt_1,
                              'B':question.opt_2, 'C':question.opt_3, 'D':question.opt_4, 'correct':question.correct_answer-1,
                              'given': answer})
            question.save()
        snap_shot_list = json.dumps(snap_shot)
        instance.snapshot = json.dumps({'question_list': snap_shot_list})
        if session.has_penalty():
            penalties = len(wrong_answered)/session.penalized_for()
        score = 100*(len(correctly_answered_questions)-penalties)/questions.count()
        instance.score = score
        instance.not_answered = not_answered
        instance.wrong_answers = wrong_answered
        ## to be used for checking pass/fail
        exam_session = instance.get_session()

        f_session = None
        instance.is_passed = False
        if exam_session.session_ref_number.startswith('course'):
            exam = exam_session.course_exam
            if exam_session.course_exam_fsessions.all().count() > 0:
                f_session = exam_session.course_exam_fsessions.first()
        elif exam_session.session_ref_number.startswith('sub'):
            exam = exam_session.subject_exam
            if exam_session.sub_exam_fsessions.all().count() > 0:
                f_session = exam_session.sub_exam_fsessions.first()
        if instance.score >= exam.pass_score:
            instance.is_passed = True

        if exam_session.show_score:
            instance.show_score = True

        if f_session:
            instance.fsession_ref_number = f_session.session_ref_number



@receiver(post_save, sender=ExamResults) 
def finish_send_score(sender, instance, created, **kwargs):
    """
    This method sends score to Netrise application.
    """
    if instance.is_finished and instance.score != None:
        if instance.fsession_ref_number:
            ref_code = instance.fsession_ref_number
        else:
            ref_code = instance.session_ref_number
        nid = instance.student.username
        score = str(int(instance.score))
        d_date = str(instance.get_session().exam_start.date())
        t_date = str(instance.get_session().exam_start.time())
        date = d_date + ' ' + t_date
        passed = str(int(instance.is_passed))
        if instance.is_abscent:
            status = 1
        else:
            status = 0
        try:
            course_name = instance.get_session().get_course()
            if course_name == 'IR(A)' or course_name == 'IR(H)':
                URL = 'https://bpms.cao.ir/NetForm/Service/irexamresult/request'
            else:
                URL = 'https://bpms.cao.ir/NetForm/Service/examresult/request'
            send_score(ref_code, nid, score, date, passed=passed, status=status, url=URL)
            
        except:
            pass



def re_sort(quests):
    sorted = {}
    i=1
    for q in quests:
        sorted[i] = q.question_ref_code
        i+=1
    return sorted
        
        
            
        







