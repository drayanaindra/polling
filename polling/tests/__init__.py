import unittest
import pkgutil

# uncomment below for manual discovery
# from test_forms import *
# from test_models import *
# from test_views import *

# uncomment below for automatic discovery
def suite():
    """ automatically detect folder"""
    return unittest.TestLoader().discover("polling.tests", pattern="*.py")
