""" Add models to django admin page """

from django.contrib import admin

from polling.models import Question, Choice, Answer

admin.site.register(Question)
admin.site.register(Choice)
admin.site.register(Answer)