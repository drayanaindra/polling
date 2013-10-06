from django import template
from django.utils.html import escape
from django.template import Variable, Library, Node, TemplateSyntaxError, TemplateDoesNotExist, VariableDoesNotExist
from django.conf import settings

from polling.models import Question, Choice

register = template.Library()

@register.simple_tag    
def total_poll_count(token):
    """ count the total poll from user (user) 
    
    usage: ::
    
        {{ request.user | total_poll_count }}
        
    """
    return Question.objects.total_poll_count(token)

@register.inclusion_tag('polling/latest.html')
def latest_poll(token):
    """ get latest_poll 
    
    :returns: list with latest_poll , choices, and boolean whether user is authorized 
    
    .. warning ::
        
        this function is deprecated and not supported on further release
        
    """
    poll = None
    choices = None
    is_auth = None
    if Question.objects.all().count():
        poll = Question.objects.all().order_by("-created_on")[0:1]
        choices = Choice.objects.filter(question = poll[0])
        is_auth = token
    return {"latest_poll":poll, "choices": choices, "is_auth": is_auth}