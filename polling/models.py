"""
Models that are created for polling app

"""
import re
import time
import datetime

from django.db import models
from django.contrib.auth.models import User

class PollManager(models.Manager):
    def total_poll_count(self, user):
        """ adding query to get how many poll created by spesific user """
        return Question.objects.filter(created_by=user).count()

class Question(models.Model):
    """ Question where Poll Question is saved """
    title = models.CharField(max_length = 200)
    #: to display on get in address bar max 200 characters
    slug = models.SlugField(unique = True, max_length = 200)
    text = models.TextField()
    #: add additional functions when calling Question.objects
    objects = PollManager()
    created_by = models.ForeignKey(User)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def save(self,*args,**kwargs):
        """ make sure the slug is created when model is saved """
        # change title to fit in slug
        self.slug = self.change_title_to_slug(self.title)
        super(Question, self).save(*args,**kwargs)
    
    def change_title_to_slug(self,title = ""):
        """ change title name to fit in slug requirements 
        
        :param title: title string to feed the slug OR use default,
                      because calling self.title in argument is not possible,
                      as alternative call after self is defined.
        """
        title = title if title is not "" else self.title
        
       # if title slug is already exist, increase the count number
        slug = re.sub(r'\W+', '-', title)
        count = Question.objects.filter(slug__icontains = slug).count()
        if count > 0:
            slug += str(count+1)
        return slug
    
    def __unicode__(self):
        """ return string presentation <title>"""
        return self.title
    
    class Meta:
        ordering = ('-created_on', )
    
class Choice(models.Model):
    """ Where user created choices are kept 
    
    .. note ::
        
        user choices is not kept to provide user anonymity (privacy)
    
    """
    question = models.ForeignKey(Question)
    text = models.CharField(max_length=100)
    total_votes = models.IntegerField(default = 0)
    
    def __unicode__(self):
        """ return string presentasion with format: <title> -  <text>"""
        return '%s - %s' % (self.question.title, self.text)
    
    def update_total_votes(self):
        """ update additional 1 votes  """
        self.total_votes += 1
        self.save()

class Answer(models.Model):
    """ Keep track answered poll by user """
    #: connected with question model
    question = models.ForeignKey(Question)
    #: connected with user table, call its object not its id
    answered_by = models.ForeignKey(User)
    #: get current time
    answered_on = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        rformat = "%d/%m/%Y %H:%M"
        return '%s answered %s on %s' % (self.answered_by, self.question.title, self.answered_on.strftime(rformat))