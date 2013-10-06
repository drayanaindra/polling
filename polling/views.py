"""
views is a Controller for user interface of the app

"""
import pdb
import re 

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.views.generic import FormView,ListView,DeleteView,DetailView,TemplateView,View
from django.utils.decorators import method_decorator

from polling.forms import CreatePollQuestion
from polling.models import Question,Answer,Choice,PollManager

class PollQuestion(DetailView):
    """ Define a View where user can vote """
    template_name = 'polling/question.html'
    context = None
    
    @method_decorator(login_required)
    def get(self, request, slug):
        """
        using @method_decorator(login_required) because if user not authorized, app will
        redirect user to login form (using django-registration)
        """
        question = Question.objects.get(slug = slug)
        choices = Choice.objects.filter(question__slug = slug)
        context = {
            'question':question,
            'choices':choices
        }
        
        if Answer.objects.filter(answered_by=request.user, question=question):
            return HttpResponseRedirect(reverse('polling:tappolling_results', args=[question.slug]))

        return render_to_response(
                'polling/question.html',
                context, 
                context_instance=RequestContext(request),
            )

    def post(self, request, slug):
        """ Define the result when user has voted 
        
        :returns: user has voted, redirect to vote result and stay on the page if otherwise
        
        """
        question = Question.objects.get(slug = slug)
        choices = Choice.objects.filter(question__slug = slug)
        context = {
           'question':question,
           'choices':choices,
           'error':'please choose one'
        }
        
        form_error = False
        if not Answer.objects.filter(answered_by=request.user, question=question):
            if request.POST.get('choices', None):
                choice_id = int(request.POST['choices'])
                
                choices = Choice.objects.filter(id=choice_id)
                
                for choice in choices:
                    choice.update_total_votes()
                
                answer = Answer(answered_by=request.user, question=question)
                answer.save()

                return HttpResponseRedirect(reverse('polling:tappolling_results',args=[question.slug]))
            else:
                # returns to the same page with error
                return render_to_response( self.template_name, context,context_instance=RequestContext(request)) 

class PollResults(View):
    """ Show vote result """
    
    def get(self,request,slug):
        """ show the poll result, chart is rendered front side. Server / backend
        only need to throw poll data in a list.
        
        :returns: rendered page
        """
        question = get_object_or_404(Question,slug=slug)
            
        total_votes = 0
        data_list=[]
        
        for choice in question.choice_set.all():
            total_votes += choice.total_votes
            text = choice.text.replace("'","\\'")
            data_list.append((re.sub(r"'","\\'",choice.text) ,choice.total_votes)) 

        # used for render title in javascript
        jstitle = question.title.replace("'","\\'")
        
        context = {'question':question,
                   'total_votes':total_votes, 
                   'jstitle':jstitle,
                   'data_list':data_list,
                   'poll_slug':slug}

        return render_to_response(
                  'polling/poll_results.html', 
                  context, 
                  context_instance=RequestContext(request))
    
class DeletePollView(DeleteView):
    """ called when Quesiton object wants to be deleted """
    model=Question
    success_url=reverse_lazy('polling:question_list')
    
    def get(self, request, *args, **kwargs):
        """ safe guard for GET to make sure anybody beside the owner, can not delete poll """
#         questions = Question.objects.filter(pk=kwargs['pk'])
        question = get_object_or_404(Question,pk=kwargs['pk'])
        if question.created_by == request.user :
            return DeleteView.get(self, request, *args, **kwargs)
        else :
            return HttpResponseForbidden('you are not allowed to do this')
    
    def post(self, *args, **kwargs):
        """ safe guard for POST to make sure only owner can delete his own poll """
        question = get_object_or_404(Question,pk=kwargs['pk'])
        
        if question.created_by == self.request.user :
            return DeleteView.post(self, *args, **kwargs)
        else :
            return HttpResponseForbidden('you are not allowed to do this')

class CreatePollView(FormView):
    """ class based Create poll view where user can create a Poll Question """
    
    template_name = 'polling/poll_create_form.html'
    form_class = CreatePollQuestion
    args=[]
    
    def get_context_data(self, **kwargs):
        """ pass args form get to template as context 
        
        the add_choices context is to give how many additional input choices
        to the form
        
        """
        context = FormView.get_context_data(self, **kwargs)
        
        # checking from POST request
        request_choice = self.request.POST.get('request_choice',0)
        last_choice = int (request_choice) - 2 if request_choice else 0
        
        # assign from last_choice, ignore from GET, because input from POST
        # from javascript has higher precedence than GET
        if last_choice :
            context['add_choices'] =  last_choice
        else :
            # checking from arguments (GET)
            # get previous total choices in the form, if exist
            previous = int(self.args[1])if len (self.args) == 2 else 0
            context['add_choices'] = int(self.args[0]) + previous if len(self.args) > 0 else 0
        
        return context 
    
    @method_decorator(login_required)
    def get(self, request, *args, **kwargs):
        """ a safe guard to make sure that user is already authenticated
        
        :returns: if user is authenticated return form page OR return to form user login
        using overiding @method_decorator(login_required)
                  
        """
        self.args=args
        if self.request.user.is_authenticated():
             return FormView.get(self, request, *args, **kwargs)

    
    def form_valid(self, form):
        """ check whether the form is valid or not using CreatPollQuestion
         
        :param form: defined in form_class
        :returns: Redirect to recently created poll
        
        """
        question = form.save(self.request.user)
        
        return HttpResponseRedirect( reverse('polling:tappolling_question', 
                                             args=[question.slug] ))

class QuestionListView(ListView):
    """ A list of available Questions """
    template_name="polling/poll_question_list.html"
    context_object_name="poll_questions"
    
    def render_to_response(self, context, **kwargs):
        """ Override to include request context """
        return super(QuestionListView, self).render_to_response(
                RequestContext(self.request,
                               context,
                               ),
                **kwargs)
        
    def get_queryset(self):
        """ show query for the Question model
        
        :returns: all Question object 
        
        """
        return Question.objects.all() 
