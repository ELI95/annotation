from django.conf.urls import url

from .views import (
    QuizAPIView,
    QuizAPIDetailView,
    QuestionAPIView,
    AnswerAPIView,
    QuizRecordView,
)


urlpatterns = [
    url(r'^$', QuizAPIView.as_view(), name='list'),
    url(r'^(?P<id>\d+)/$', QuizAPIDetailView.as_view(), name='detail'),
    url(r'^(?P<id>\d+)/questions/$', QuestionAPIView.as_view(), name='question-list'),
    url(r'^(?P<id>\d+)/answer/$', AnswerAPIView.as_view(), name='answer'),
    url(r'^(?P<id>\d+)/records/', QuizRecordView.as_view(), name='record-list'),
]
