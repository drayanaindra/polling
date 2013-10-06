import random
import string

from django.contrib.auth.models import User,UserManager
from django.core.urlresolvers import reverse

from polling.models import Question, Choice, Answer
from polling.forms import CreatePollQuestion

# models
def create_user(username,password):
    """ create user for testing """
    return User.objects.create_user(username=username,password=password)

def create_question(user,title='title',text='text'):
    """ create data that use Question model """
    return Question.objects.create(created_by=user, title=title, text=text)

def create_choices(question_model, text="text", total_votes = 0):
    """ create data that use Choice model """
    return Choice.objects.create(question=question_model, 
                                 text=text, 
                                 total_votes=total_votes)

def create_answer(question, user):
    """ create data that use Answer model """
    return Answer.objects.create(question=question,answered_by=user)

def create_user_using_manager(username,password):
    """ same as create_user but using user manager """
    manager = UserManager()
    return manager.create_user(username=username, password=password)
    
def create_random_user(total):
    for i in range(total):
        create_user(
            create_random_string(5),
            create_random_string(10))
        
def create_random_string(total_character):
    """ create random string using string.printable
    
    :param total_character: how long the string will be
    :type total_character: integer
    
    """
    feed=string.printable
    words=""
    i=0
    while i < total_character:
        words += feed[random.randrange(0,len(feed)-1)]
        i+=1
    return words

def seed_random(max_integer):
    """ give random value between 0 ~ max """
    return random.randrange(0,max_integer);

def populate_poll(user="",total=10):
    """ populate question object with random string and user 
    
    :param user: user object
    :param total: an integer to describe how many data to be made
    
    """
    user_list = None
    #create random user only when user argument empty
    if user == "":
        create_random_user(20)
        user_list = User.objects.all()
    
    for i in range(total):
        Question.objects.create(
            created_by=random.choice(user_list) if user_list is not None else user,
            title=create_random_string(seed_random(10)),
            text=create_random_string(seed_random(300)),
            slug=create_random_string(seed_random(100)) ) 
    
def create_dummy_form(title,text,fill_choice=[],choice_length=[]):
    """ create CreatePollQuestion dummy form
    
    :param title: the title to put on question_title
    :type title: string
    :param text: text to put on question_description
    :type text: string
    :param fill_choice: choices to fill with a dummy text
    
    """
    # fill it with blank for dummy choices
    count=0
    choices=[]
    while count < 8:
        choices.append(None)
        count+=1
    
    # fill choices based on value on fill_choice
    for i in fill_choice:
        try :
            length = choice_length[i]
        except IndexError :
            length = 10
        choices[i] = create_random_string(length)

    dummy_form=CreatePollQuestion(
                  {"question_title":title,
                   "question_text" :text,
                   "choice_1":choices[0],
                   "choice_2":choices[1],
                   "choice_3":choices[2],
                   "choice_4":choices[3],
                   "choice_5":choices[4],
                   "choice_6":choices[5],
                   "choice_7":choices[6],
                   "choice_8":choices[7],
                   })

    return dummy_form