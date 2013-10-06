"""
    A Reusable tags that hopefully will useful accross many projects
"""
import pdb
from django.template import Library

register = Library()

@register.filter(name="get_range")
def get_range( value ):
    """ Filter - returns a list containing range made from given value created by zalun
      
      usage (in template): ::
    
          <ul>{% for i in 3|get_range %}
            <li>{{ i }}. Do something</li>
          {% endfor %}</ul>
    
      Results with the HTML: ::
      
          <ul>
            <li>0. Do something</li>
            <li>1. Do something</li>
            <li>2. Do something</li>
          </ul>
    
      Instead of 3, any number may use the variable set in the views (need to change the source) 
    """
    #for multiple arguments
    start = 3
    return range( start, value+start )


@register.filter(is_safe=True)
def if_exist( var , output):
    """ if value is true return output, this is the opposite of default tag in django. 
    
    :param var: common variables
    :param output: string output
    
    assume context sent a variable name ``check``, usage(in template): ::
        
        {{ check | if_exist:"show me something" }}
        
    
    Results :
    When chek is ``True`` show ``show me something`` and when ``False`` returns an empty string
    
    """
    if var :
        return output
    else :
        return "" 
    

@register.filter()
def check_exist(search, datas):
    """ check string in list such ((x,y),(a,b))
    then show result on match.
    
    :param search: a key value to search , the first index
    :param datas: a list of data
    
    assume datas has (('a',b'),('c','d')). then when user do in template ::
    
        {{ "a" | check_exist }}
        
    ``b`` will be shown when exist, or return nothing when couldn't find a match
     
    """
    # using normal search algorithm method
    # may need to improve the algorithm for further fast searching
    result = []
#     pdb.set_trace()
    if len(datas) > 0:
        for data in datas:
            if data[0] == search:
                result = data
                return result[1]
    return