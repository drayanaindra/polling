from django import forms
import models
import pdb

class CreatePollQuestion(forms.Form):
    """ Create Poll Question Form and define its attribute and functions """
    question_title = forms.CharField(
        max_length=200,
        help_text = 'Title for your poll. This is required.', 
        widget=forms.TextInput())
    
    question_text = forms.CharField(
        widget = forms.Textarea(), 
        help_text = 'Some description. This is required.')
    
    choice_1 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(),
        help_text = 'Allowed choices for the poll. At least two are required.')
    
    choice_2 = forms.CharField(
        max_length=100,
        widget=forms.TextInput(),)
    
    def clean(self):
        """ add new error on extra choices beside choice_1 and choice_2 """
        
        cleaned_data = super(CreatePollQuestion,self).clean()
        
        # remove cleaned data
        for data,value in self.data.items():
            if data not in ["csrfmiddlewaretoken",
                            'question_title',
                            'question_text',
                            'request_choice',
                            'choice_1',
                            'choice_2'
                            '']:
                length = len(value) if value else 0
                if length > 100 :
                    self._errors[data]= self.error_class([u"Ensure characters has no more than 100 (it has %s)" %(length)])
        return cleaned_data
    
    def save(self, user):
        """ Save current Poll and assign clean data to save it to database
        
        .. Warning::
           
           Only call save() when form is valid, failure to do so may cause 
           undesirable error that is cleaned_data not exist, as cleaned_data
           only occur when the form is valid
        
        :param user: user information
        :returns: Question Models with recently saved data
        
        """
        
        question = models.Question(
           created_by=user, 
            title = self.cleaned_data['question_title'], 
            text = self.cleaned_data['question_text'])
        
        question.save()

        # get additional data and save it to database
        # TODO need improvement as checking for data error still not exist
        for data,value in self.data.items():
            choice = None
            if data not in ["csrfmiddlewaretoken",
                            'question_title',
                            'question_text',
                            'request_choice',
                            '']:
                # make sure required value are saved using cleaned_data
                if data in ['choice_1','choice_2'] :
                    choice = models.Choice(
                       question = question,  
                       text = self.cleaned_data[data])
                elif value:
                    choice = models.Choice(
                           question = question,
                           text = value )
                
                # make sure choice is not empty
                if choice is not None:
                    choice.save()
            
        return question
    