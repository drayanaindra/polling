from django.conf.urls import patterns, include, url
from django.contrib import admin
from polling.views import QuestionListView
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', QuestionListView.as_view()),
    # url(r'^demo/', include('demo.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^account/', include('registration.backends.default.urls')),
    url(r'^poll/',include('polling.urls',namespace="polling")),
)
