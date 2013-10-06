*********************
Polling User Guide
*********************

A Polling app that focus on create a poll and allow user to vote.

.. note ::
    
    Source code written using PEP Convention, we espect to you follow it when
    add a modification to the code.

Feature
=======

Features for this application are:

* Create, Delete and View a poll 
* Multiple choices to create

Installation
============
use this command to install only django dependecies ::
	
	$ pip install -r django_requirements.txt

or use the setup.py ::

    $ pip install setup.py
    
add ``polling`` to INSTALLED_APPS in ``setting.py`` ::

	INSTALLED_APPS = (
	...
	'polling',
	)

synchronize the database ::

	$ python manage.py syncdb
	
Setting Up
==========
This app use a Google API Chart to create Pie Chart using javascript. Thus, it is
required that browser has cappability to run javascript and connected to internet.

Setting up base.html
--------------------
in parent base.html, use the following structure in the app (google API chart is required when you want to use it) ::


    <head> 
        ...
        {%block stylesheet%}{%endblock stylesheet%}
        <!-- jquery -->
        <script src="http://code.jquery.com/jquery-1.10.1.min.js"></script>
        <!-- google API Chart -->
    	<script type="text/javascript" src="https://www.google.com/jsapi"></script>
    </head>
    <body>
        ...
        {%block scripts%} {%endblock scripts%}
    </body>
    
Changing chart script
---------------------
To change Google APi Chart, add the chart script on ``<head>`` or in ``block scripts`` \ 
or as in the documentation of the required scripts. Then , set up the data on polling/poll_results.html. 

Pie Chart rendered using the following template: :: 
    
    [ {% for data, votes in data_list %} ['{{data}}', {{votes}}],{%endfor%} ];
    
Result in javascript: ::
    
    [['<data>',<value>],['<data>',<value>], ... ]

Change that to fit on your chart script.

CSS
---
this app using twitter bootstrap 3 as css framework. To make sure that polling displayed
as in the demo, add bootstrap on ``<head>``.

    
