from django.urls import re_path
from exam_sessions.views import ResultDetailView, sending_score,list_participants, start_session, register_status


urlpatterns = [
    re_path(r'^transcript/(?P<pk>\d+)$', ResultDetailView.as_view(), name='result-detail'),
    re_path(r'^score-send/(?P<pk>\d+)$', sending_score, name='score-send'),
    re_path(r'^participants/(?P<pk>\d+)$', list_participants, name='list-participants'),
    re_path(r'^session-start/(?P<pk>\d+)$', start_session, name='session-start'),
    re_path(r'^register-status/(?P<pk>\d+)$', register_status, name='register-status'),

]
