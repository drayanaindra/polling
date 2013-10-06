import pdb

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase
from polling.models import *
from test_definitions import *

class QuestionMethodTest(TestCase):
    
    user=None
    
    def setUp(self):
        self.user = create_user('user','pass')
        TestCase.setUp(self)
    
    def test_change_title_to_slug_using_normal_title(self):
        """ Return the same as title """ 
        q = create_question(self.user,'title','asfasdf')
        self.assertEqual(q.slug, 'title')
    
    def test_change_title_to_slug_using_mixed_word_and_non_words(self):
        """ Return omitted non words and change it with '-' """
        q = create_question(self.user,'title#^&*^#$^ok','oke')
        self.assertEqual(q.slug, 'title-ok')
    
    def test_change_title_to_slug_for_same_title_word_only(self):
        """ Returns same as title with counted equal slug at the end """
        q = create_question(self.user,'title')
        another_slug = q.change_title_to_slug("title")
        self.assertEqual(another_slug,'title2')
    
    def test_change_title_to_slug_for_mixed_words_and_non_words(self):
        """ Returns same as title and omitted non words with counted equal slug at the end """
        q = create_question(self.user,'title334(*&#*(&*(#@ok')
        another_slug= q.change_title_to_slug('title334(*&#*(&*(#@ok')
        self.assertEqual(another_slug,'title334-ok2')
    
    def test_change_title_to_slug_for_first_mixed_second_not_mixed(self):
        """ Returns same as title and omitted non words with counted equal slug at the end """
        q = create_question(self.user,'Hello ?')
        another_slug=q.change_title_to_slug('Hello')
        self.assertEqual(another_slug, 'Hello2')
    
    def test_change_title_to_slug_same_words_different_case(self):
        """ Return the same as title with counted equal slug at the end"""
        q = create_question(self.user,"Test")
        another_slug=q.change_title_to_slug('test')
        self.assertEqual(another_slug,'test2')
        
    def test__unicode__normal_string(self):
        """ Return unicode string of the title """
        q = create_question(self.user,"test")
        self.assertEqual(q.__unicode__(), u'test')
    
    def test__unicode__mixed_string(self):
        """ Return unicode string of the title """
        q = create_question(self.user,"test123?")
        self.assertEqual(q.__unicode__(), u'test123?')
        
class ChoiceMethods(TestCase):
    
    question=None
    
    def setUp(self):
        user = create_user('user','pass')
        self.question = create_question(user,'test','test')
        TestCase.setUp(self)
    
    def test__unicode__normal_string(self):
        c = create_choices(self.question,'text')
        self.assertEqual(c.__unicode__(), u'test - text')
        
    def test__unicode__mixed_string(self):
        c = create_choices(self.question,'text ?')
        self.assertEqual(c.__unicode__(), u'test - text ?')
        
    def test_update_total_votes_1_times(self):
        create_choices(self.question,'One')
        results = Choice.objects.filter(text="One")
        # updating 1 times
        results[0].update_total_votes()
        self.assertEqual(results[0].total_votes, 1,"fail on 1")
        
    def test_update_total_votes_99_times(self):
        c = create_choices(self.question,'test')
        results = Choice.objects.filter(text="test")
        # updating 99 times
        for i in range(99) :
            results[0].update_total_votes()
        self.assertEqual(results[0].total_votes, 99,"fail on 99")
    
    def test_update_total_votes_300_times(self):
        c = create_choices(self.question,'this is sparta!!!')
        results = Choice.objects.filter(text="this is sparta!!!")
        
        # updating 300 times
        for i in range(300) :
            results[0].update_total_votes()
        self.assertEqual(results[0].total_votes, 300,"fail on 300")
        
class AnswerMethods(TestCase):
    
    user = None
    question = None
    
    def setUp(self):
        self.user = create_user('user','pass')
        self.question = create_question(self.user,'test','test')
        TestCase.setUp(self)
    
    def test__unicode__normal_string(self):
        a = create_answer(self.question,self.user)
        now = timezone.now()
        
        rformat = "%d/%m/%Y %H:%M"
        self.assertEqual(a.__unicode__(), u"user answered test on "+now.strftime(rformat))
        
class PollManagerMethod(TestCase):
    user = None
    def setUp(self):
        self.user = create_user(username="user",password="pass")
#         create_question(user,'test');
        
    def test_total_poll_count(self):
        populate_poll(self.user,10)
        total = Question.objects.total_poll_count(self.user)
        self.assertEqual(total, 10)
        
        populate_poll(self.user,20)
        total = Question.objects.total_poll_count(self.user)
        # total 30 because first: 10, second: 20
        self.assertEqual(total, 30)
        
        
class QuestionModelTest(TestCase):

    """
    test case for Question model
    """
    def create_question(self, title="selamat", slug="selamat", created_by_id=1):
        return Question.objects.create(title=title, slug=slug, created_by_id=created_by_id, created_on=timezone.now())

    def test_question_create(self):
        w = self.create_question()
        self.assertTrue(isinstance(w, Question))
        self.assertEqual(w.__unicode__(), w.title)