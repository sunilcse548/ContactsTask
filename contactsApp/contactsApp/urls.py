from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('contactsApp.views',
    url(
        r'^facebook/login/$', 
        'fb_login', 
        name='fb_login'
    ),
    
    url(
        r'^facebook/callback/$', 
        'fb_callback', 
        name='fb_callback'
    ),   
)

urlpatterns = urlpatterns+ patterns('',
	#(r"^$", direct_to_template, {"template": "index.html"}) ,
	(r'^$', 'contactsApp.views.checkSession'),
	(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	(r"^contacts/$", direct_to_template, {"template": "contacts.html"}) ,
	
	(r"^signup/$", direct_to_template, {"template": "signup.html"}) ,

	(r"^login/$", direct_to_template, {"template": "login.html"}) ,
	#userSignup
	 (r'^userSignup/$', 'contactsApp.views.userSignup'),
	#userLogin
	(r'^userLogin/$', 'contactsApp.views.userLogin'),
	#userLogout
	(r'^userLogout/$', 'contactsApp.views.userLogout'),
        #addContact
	(r'^addContact/$', 'contactsApp.views.addContact'),
	#deleteContact
	(r'^deleteContact/$', 'contactsApp.views.deleteContact'),
	#updateContact
	(r'^updateContact/$', 'contactsApp.views.updateContact'),
)
#
