from django.apps import AppConfig


class ExamSessionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'exam_sessions'

    def ready(self):
        import exam_sessions.signals