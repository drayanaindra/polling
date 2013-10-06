import pdb

from django.test import TestCase
from django.test.client import Client
from django.test.utils import override_settings
from django.core.urlresolvers import reverse_lazy, reverse

from polling.views import *
from test_definitions import *

class QuestionViewTest(TestCase):
    def setUp(self):
        user = create_user('user','pass')
        create_question(user, 'test','test')
        TestCase.setUp(self)

    def test_call_question_list_anonymous(self):
        """
        TestCase for view polling list if not auth user login
        should display question list page
        """
        response = self.client.get(reverse('polling:question_list'))
#       pdb.set_trace()
        self.assertEqual(response.status_code, 200)
        # should display polling/question_list
        self.assertTrue("polling/question_list.html" in response.template_name)

    def test_call_question_list_with_auth_user(self):
        """
        TestCase for view polling list with auth user login
        should return 200 and on create page
        """
        # login
        client = self.client.login(username='user',password='pass')
        # request to create poll
        response = self.client.get(reverse("polling:question_list"))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request['PATH_INFO'],'/poll/')

class CreatePollViewTest(TestCase):

    def setUp(self):
        user = create_user('user','pass')
        create_question(user, 'test','test')
        TestCase.setUp(self)
        
    def test_call_redirected_when_calling_create_with_unauth_login(self):
        """
        TestCase for view polling list with auth user login
        should redirected to login page
        """
        response = self.client.get(reverse('polling:create'))
        self.assertTrue(response.status_code,302)
        self.assertTrue( response['location'].find('/accounts/login'))
        
    def test_call_create_when_auth(self):
        """ show status_code 200 and goto create page """
        
        client = self.client.login(username='user',password='pass')
        response = self.client.get(reverse('polling:create'))
        
        self.assertTrue(response.status_code,200)
        # should request a poll/create page
        self.assertTrue(response.request['PATH_INFO'],'/poll/create/')
        
    def test_form_valid(self):
        success= self.client.login(username='user',password='pass')
        self.assertTrue(success)
        
        response = self.client.post(reverse('polling:create'),
                                    {'question_title':'test_123',
                                     'question_text':'test',
                                     'choice_1':'test',
                                     'choice_2':'test'})
        # redirected to votes page
        self.assertEqual(response.status_code,302)
        # check objects Question
        qobject = Question.objects.filter(title="test_123")
        self.assertTrue(qobject)
        
class DeletePollViewTest(TestCase):
    def setUp(self):
        create_user('user','pass')
        create_user('owner','pass')
        TestCase.setUp(self)
    
    def test_delete_from_auth_not_owner(self):
        # login as user
        self.client.login(username='user',password='pass')
        # create poll using owner
        user = User.objects.get(username='owner')
        
        create_question(user,'test','test')
        question = Question.objects.get(title='test')
        
        # using GET
        response = self.client.get(reverse('polling:delete',args=[question.id]))
        self.assertEqual(response.status_code,403)
        
        # using POST
        response = self.client.post(reverse('polling:delete',args=[question.id]))
        self.assertEqual(response.status_code,403)
        
    def test_delete_on_not_exist(self):
        response = self.client.get(reverse('polling:delete',args=[111]))
        self.assertEqual(response.status_code, 404 )
    
    def test_delete_from_auth_and_owner(self):
        self.client.login(username='owner',password='pass')
        user = User.objects.get(username='owner')
        
        create_question(user,'test_delete','test')
        question = Question.objects.get(title='test_delete')

        # still in the page
        response = self.client.get(reverse('polling:delete',args=[question.id]))
        self.assertEqual(200,response.status_code)
        
        # redirected when success to question_list
        response = self.client.post(reverse('polling:delete',args=[question.id]))
        self.assertRedirects(response, 
                             reverse('polling:question_list'), 
                             status_code=302)