from django.db import models
from questions.models import QuestionModel, CourseExamModel, SubjectExamModel, PerSubjectModel
from users.models import CustomUser
from django.db.models import JSONField


class AbstractExamSession(models.Model):
    session_name = models.CharField(
        "Session name", max_length=20, default="New Session")

    session_descriptions = models.CharField(
        "Session descriptions", max_length=150, default="Description")

    session_ref_number = models.CharField("Session reference code", max_length=20, blank=True,
                                          editable=False, unique=True)
    
    exam_start = models.DateTimeField("Exam start time")
    strict_timing = models.BooleanField("Strict Timing", default=False)
    show_score = models.BooleanField(
        "Show scores at the end to the applicant?", default=False)
    questions = models.ManyToManyField(QuestionModel)
    is_active = models.BooleanField("Is active session?", default=True)
    session_total_seats = models.PositiveIntegerField("Total number of seats", blank = True,
                                                      null = True)
    session_occupied_seats = models.PositiveIntegerField("Number of occupied seats", blank = True,
                                                      default = 0)
    

    class Meta:
        abstract = True

    # @classmethod
    # def get_user_sessions(cls, user=None):
    #     """
    #     This function gets active exam sessions of a user based on the user identified in keyword arguments.
    #     """
    #     if user:
    #         active_sessions = cls.objects.filter(is_active=True)
    #         user_active_sessions = []
    #         for active_session in active_sessions:
    #             if user.groups.filter(name=active_session.participants.name).exists():
    #                 user_active_sessions.append(active_session)
    #         return user_active_sessions
    #     else:
    #         return None


class CourseExamSession(AbstractExamSession):
    course_exam = models.ForeignKey(
        CourseExamModel, on_delete=models.CASCADE, related_name="sessions_course_exams")
    participants = models.ManyToManyField(CustomUser, verbose_name="Exam participant",
                                          related_name="course_exams")
    

    def course_name(self):
        return self.course_exam.course.course_name
    
    def session_occupied_seats(self):
        return self.participants.all().count()
    
    def get_course(self):
        return self.course_exam.course.course_name
    
    def has_penalty(self):
        return self.course_exam.has_penalty
    
    def penalized_for(self):
        return self.course_exam.penalize_for

    def remaining_seats(self):
        if self.course_exam_fsessions.count() == 0:
            """
            +1 for saving the instance in admin
            """
            return self.session_total_seats - self.session_occupied_seats() + 1
        else:
            return 1
    
        

    def __str__(self):
        return self.course_exam.course.course_name + '-' + self.session_ref_number


class SubjectExamSession(AbstractExamSession):
    subject_exam = models.ForeignKey(
        SubjectExamModel, on_delete=models.CASCADE, related_name="sub_exam_sessions")
    participants = models.ManyToManyField(CustomUser, verbose_name="Exam participant",
                                          related_name="subject_exams")

    def __str__(self):
        return self.subject_exam.exam_name + '-' + self.session_ref_number
    
    
    def session_occupied_seats(self):
        return self.participants.count()
    
    def remaining_seats(self):
        return self.session_total_seats - self.session_occupied_seats()
    
    def has_penalty(self):
        return self.subject_exam.has_penalty
    
    def penalized_for(self):
        return self.subject_exam.penalize_for
    
class FreeExamSession(models.Model):
    session_ref_number = models.CharField("Session reference code", max_length=20, blank=True,
                                          editable=False, unique=True)
    subject_sessions = models.ManyToManyField(SubjectExamSession, verbose_name="Included Subject Exams",
                                              related_name="sub_exam_fsessions")
    course_sessions = models.ManyToManyField(CourseExamSession, verbose_name="Included Course Exams",
                                              related_name="course_exam_fsessions")
    exam_start = models.DateTimeField("Exam start time")
    show_score = models.BooleanField(
        "Show scores at the end to the applicant?", default=False)
    is_active = models.BooleanField("Is active session?", default=True)
    session_total_seats = models.PositiveIntegerField("Total number of seats", blank = True,
                                                      null = True)
    session_occupied_seats = models.PositiveIntegerField("Number of occupied seats", blank = True,
                                                      default = 0)
    
    def remaining_seats(self):
        return self.session_total_seats - self.session_occupied_seats
    
    def increment_occupied(self):
        self.session_occupied_seats +=1
        self.save()


    def __str__(self):
        return 'Free Session' + '-' + str(self.exam_start)
    
    class Meta:
        verbose_name = 'Free Exam Session'
        verbose_name_plural = 'Free Exam Sessions'



class ExamResults(models.Model):
    student = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="exam_results")
    session_ref_number = models.CharField("Session reference code", max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answers = JSONField("Answers", blank = True, null=True)
    wrong_answers = JSONField("Wrong Answers", blank = True, null = True)
    not_answered = JSONField("Not Answered", blank = True, null = True)
    snapshot = JSONField("Snap Shot", blank = True, null = True)
    num_wrong = models.IntegerField("Number of wrong answered questions", blank = True, null  = True)
    num_not_answered = models.IntegerField("Number of not answered questions", blank = True, null = True)
    score = models.IntegerField("Score", blank=True, null=True)
    exam_duration = models.IntegerField("Exam duration", blank=True, default=0)
    exam_remaining = models.IntegerField("Exam remaining time in seconds", blank=True, null=True)
    is_passed = models.BooleanField("Passed in exam", default=False)
    is_finished = models.BooleanField("Exam is finished", default=False)
    show_score = models.BooleanField("Show score at the end of the exam?", default=False)
    fsession_ref_number = models.CharField("Free Session reference code", max_length=20, null=True, blank=True)

    def get_session(self):
        """
        This function gets reverse appropriate session based on session reference number.
        """
        if self.session_ref_number.startswith('sub_'):
            return SubjectExamSession.objects.filter(session_ref_number=self.session_ref_number).first()
        elif self.session_ref_number.startswith('course_'):
            return CourseExamSession.objects.filter(session_ref_number=self.session_ref_number).first()
        else:
            return None
    
    def get_exam_time(self):
        session = self.get_session()
        if hasattr(session, 'subject_exam'):
            return session.subject_exam.exam_duration
        elif hasattr(session, 'course_exam'):
            return session.course_exam.exam_duration
    
    class Meta:
        unique_together = ('student', 'session_ref_number')
        verbose_name_plural = "Exam Results"


    def __str__(self):
        if self.get_session():
            return self.get_session().session_name + ' - ' + self.student.last_name
        else:
            return self.student.last_name
    
