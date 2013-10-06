import pdb

from django.test import TestCase
from django.contrib.auth.models import User

from polling.models import Question, Choice
from test_definitions import *

class CreatePollQuestionFormTest(TestCase):
    
    def test_for_error_choice_less_than_two(self):
        test = create_dummy_form("test", "test", [0])
        self.assertFalse(test.is_valid())
    
    def test_all_values_are_inputed(self):
        test = create_dummy_form("test","test",[0,1,2,3,4,5,6,7])
        self.assertTrue(test.is_valid(),                                
                        "form show an false result on all values are correct")
        
    def test_values_inputed_choice_more_than_two_less_than_max(self):
        test = create_dummy_form("test","test",[0,1,3,4])
        self.assertTrue(test.is_valid())
    
    def test_values_inputed_two_choices_on_random(self):
        test = create_dummy_form('test','test',[0,3])
        self.assertFalse(test.is_valid())
    
    def test_input_without_title(self):
        test = create_dummy_form(None,'test',[0,3])
        self.assertFalse(test.is_valid())
    
    def test_input_without_text(self):
        test = create_dummy_form('test',None,[0,3])
        self.assertFalse(test.is_valid())  
        
    def test_input_without_choice_1(self):
        test = create_dummy_form('test',None,[1,3])
        self.assertFalse(test.is_valid())
          
    def test_input_without_choice_2(self):
        test = create_dummy_form('test',None,[0,3])
        self.assertFalse(test.is_valid())
        
    def test_input_without_extra_choice(self):
        test = create_dummy_form('test','test',[0,1])
        self.assertTrue(test.is_valid())
    
    def test_input_without_required_choice(self):
        test = create_dummy_form('test','test',[2,3])
        self.assertFalse(test.is_valid())
    
    def test_input_with_150_string_on_required_choice(self):
        test = create_dummy_form('test','test',[0,1],[150,150])
        self.assertFalse(test.is_valid())
    
    def test_input_with_150_string_on_extra_choice(self):
        test = create_dummy_form('test','test',[0,1,2,3],[10,10,150,150])
        self.assertFalse(test.is_valid())
        
    def test_form_save_method_using_only_required_method(self):
        q = None
        
        test = create_dummy_form('test','test',[0,1])
        user = create_user('user','pass')
        self.assertTrue(test.is_valid())
        
        if test.is_valid():
            q = test.save(user)
        
        self.assertTrue(isinstance(q, Question))
        # count choices created 
        self.assertEqual(Choice.objects.filter(question=q).count(),2,"fail on total choices")
    
    def test_form_save_method_using_extra_choices(self):
        q = None
        
        test = create_dummy_form('test','test',[0,1,2,3,5])
        user = create_user('user','pass')
        self.assertTrue(test.is_valid())
        
        if test.is_valid():
            q = test.save(user)
        
        self.assertTrue(isinstance(q, Question))
        # count choices created
        self.assertEqual(Choice.objects.filter(question=q).count(),5,"fail on total choices")