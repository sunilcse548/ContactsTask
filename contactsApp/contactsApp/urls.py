from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

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
	
	(r'^$', 'contactsApp.views.checkSession'),
	(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),

	(r'^contacts/', TemplateView.as_view(template_name="contacts.html")),
	
	
	(r'^signup/', TemplateView.as_view(template_name="signup.html")),
	
	(r'^login/', TemplateView.as_view(template_name="login.html")),
	
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
	#paginateByAlphabet
	(r'^paginateByAlphabet/$', 'contactsApp.views.paginateByAlphabet'),
)
#
