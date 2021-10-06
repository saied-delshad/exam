from django.db import models
from questions.models import SubjectModel, CourseModel, QuestionModel, CourseExamModel, SubjectExamModel, PerSubjectModel
from users.models import CustomUser
from django.contrib.auth.models import Group
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models import JSONField


class AbstractExamSession(models.Model):
    session_name = models.CharField("Session name", max_length=20, default="New Session")

    session_descriptions = models.CharField("Session descriptions", max_length=150, default="Description")

    session_ref_number = models.CharField("Session reference code", max_length=20, blank=True,
                                          editable=False, unique=True)
    participants = models.ForeignKey(
        Group, on_delete=models.DO_NOTHING, verbose_name="Exam participants as group")
    exam_start = models.DateTimeField("Exam start time")
    strict_timing = models.BooleanField("Strict Timing", default=False)
    show_score = models.BooleanField(
        "Show scores at the end to the applicant?", default=False)
    questions = models.ManyToManyField(QuestionModel)
    is_active = models.BooleanField("Is active session?", default=True)

    class Meta:
        abstract = True
    
    @classmethod
    def get_user_sessions(cls, user=None):
        if user:
            active_sessions = cls.objects.filter(is_active = True)
            user_active_sessions =[]
            for active_session in active_sessions:
                if user.groups.filter(name = active_session.participants.name).exists():
                    user_active_sessions.append(active_session)
            return user_active_sessions
        else:
            return None


class CourseExamSession(AbstractExamSession):
    course_exam = models.ForeignKey(
        CourseExamModel, on_delete=models.CASCADE, related_name="sessions_course_exams")

    def __str__(self):
        return self.course_exam.course.course_name + '-' + self.session_ref_number


class SubjectExamSession(AbstractExamSession):
    subject = models.ForeignKey(
        SubjectModel, on_delete=models.CASCADE, related_name="sub_exam_sessions")

    def __str__(self):
        return self.subject.subject_name + '-' + self.session_ref_number


class ExamResults(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="exam_results")
    course_exam_session = models.ForeignKey(CourseExamSession, on_delete=models.DO_NOTHING,
                                            related_name="course_session", null=True)
    subject_exam_session = models.ForeignKey(SubjectExamSession, on_delete=models.DO_NOTHING,
                                             related_name="subject_sessions", null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answers = JSONField("Answers", null=True)
    score = models.IntegerField("Score", null=True)
    is_passed = models.BooleanField("Passed in exam", default=False)
    is_finished = models.BooleanField("Exam is finished", default=False)

    def __str__(self):
        if self.course_exam_session:
            return self.student.last_name + '-' + self.course_exam_session.session_ref_number
        elif self.subject_exam_session:
            return self.student.last_name + '-' + self.subject_exam_session.session_ref_number
        else:
            return self.student.last_name
