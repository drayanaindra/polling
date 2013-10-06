"""
Urls pattern to connect between html address, template, and views

"""
from django.conf.urls import patterns,url
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required
from polling.views import CreatePollView,QuestionListView,PollQuestion,PollResults, DeletePollView

urlpatterns = patterns('',

	url(r'^results/(?P<slug>[^\.^/]+)/$', PollResults.as_view(), name='tappolling_results'),
	url(r'^vote/(?P<slug>[^\.^/]+)/$', login_required(PollQuestion.as_view()), name='tappolling_question'),
   	url(r'^delete/(?P<pk>\d+)/$', DeletePollView.as_view(), name="delete"),
    url(r'^create/choices(\d+)_(\d+)/$', CreatePollView.as_view() , name='create'),
    url(r'^create/$', CreatePollView.as_view() , name='create'),
    url(r'^([\w\._-]+)/$', QuestionListView.as_view(), name='question_list'),
    url(r'^$', QuestionListView.as_view(), name='question_list'),
)