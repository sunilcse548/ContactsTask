import cgi
import json
import urllib
import logging

from django.conf import settings
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, HttpResponseRedirect
from django.template import RequestContext
#from .models import FacebookProfile
import models
from models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required

def add_user(username, password, email):
    user = User.objects.create_user(
        username=username, 
        password=password, 
        email=email
    )
    user.is_active = True
    user.save()
    return user


def create_fb_profile(id, fb_id, access_token):
        FacebookProfile.objects.create(
              user_id=id, 
              facebook_id=fb_id, 
              access_token=access_token
        )    


def get_profile(request, token=None):
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'client_secret': settings.FACEBOOK_APP_SECRET,
        'redirect_uri': request.build_absolute_uri(reverse('fb_callback')),
        'code': token,
    }

    target = urllib.urlopen('https://graph.facebook.com/oauth/access_token?' + urllib.urlencode(args)).read()
    response = cgi.parse_qs(target)
    logging.warning(target);
    logging.warning(response);
    access_token = response['access_token'][-1]
   
    return access_token


def fb_login(request):
    args = {
        'client_id': settings.FACEBOOK_APP_ID,
        'scope': settings.FACEBOOK_SCOPE,
        'redirect_uri': request.build_absolute_uri(reverse('fb_callback')),
    }
    return HttpResponseRedirect('https://www.facebook.com/dialog/oauth?' + urllib.urlencode(args))


def fb_callback(request):
    error = request.GET.get('error')
    if(error):
         return HttpResponseRedirect('/')
    access_token = get_profile(request, request.GET.get('code'))   
    fb_profile = urllib.urlopen('https://graph.facebook.com/me?access_token={0}'.format(access_token))
    fb_profile = json.load(fb_profile)
    
    try:
        fb_user = FacebookProfile.objects.get(facebook_id=fb_profile['id'])
        fb_user.access_token = access_token
        fb_user.save()
        
        user = User.objects.get(pk=fb_user.user_id)
        user.backend = 'django.contrib.auth.backends.ModelBackend'

        if user.is_active:
            auth_login(request, user)
            return HttpResponseRedirect('/contacts/')
        else:
            return HttpResponseRedirect(reverse('accounts:login'))
    except FacebookProfile.DoesNotExist:
        logging.warning(fb_profile)
        fb_username = fb_profile.get('username', fb_profile['email'].split('@')[0])
        fb_id = fb_profile['id']
        fb_email = fb_profile['email']
        
        user = add_user(fb_username, fb_username, fb_email)
        create_fb_profile(user.id, fb_id, access_token)
        
        user = authenticate(username=fb_username, password=fb_username)

        auth_login(request, user)
        request.session["user"] = fb_username
        print request.session["user"]
        return HttpResponseRedirect('/contacts/')

def userLogin(request):
     username = request.POST.get('username')
     password = request.POST.get('password')
     user = authenticate(username=username, password=password)
     auth_login(request, user)
     request.session["user"] = username
     print request.session["user"]
     return HttpResponseRedirect('/')

def userLogout(request):
     logout(request)
     return HttpResponseRedirect('/')


def userSignup(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    confirmPassword = request.POST.get('confirmPassword')
    if(len(password)>6):
          if(password==confirmPassword):
        
                if email:
                      testUser = User.objects.filter(username=email)
                      if testUser:
                            return render_to_response( 'signup.html', {"error":"A user already exists with provided email id. Use another one"},context_instance=RequestContext(request))
                      add_user(email,password,email)
                      #return render_to_response( 'index.html', {"error":"User created. Login from here"},context_instance=RequestContext(request))
                      user = authenticate(username=email, password=password)

                      auth_login(request, user)
                      request.session["user"] = email
                      print request.session["user"]
                      contactsList = contacts.objects.filter(user=user)
                      logging.warning(contactsList)
                      return render_to_response( 'contacts.html', {},context_instance=RequestContext(request))#return HttpResponseRedirect('/contacts/')
                else:
                      return render_to_response( 'signup.html', {"error":"Invalid Email"},context_instance=RequestContext(request))
          else:	
                return render_to_response( 'signup.html', {"error":"Password and confirm password does not matches"},context_instance=RequestContext(request))
    else:
         return render_to_response( 'signup.html', {"error":"Password length cannot be less than 6 chars"},context_instance=RequestContext(request))

def checkSession(request):
    currentUser = ''
    try:
         currentUser = request.session["user"]
    except :
        print "No session"
    if currentUser:
        loggedInUser = User.objects.get(username = currentUser)
        contactsList = contacts.objects.filter(user=loggedInUser)
        #logging.warning(contactsList)
        if contactsList:
            for x in contactsList:
                print x
            paginator = Paginator(contactsList, 10)
            page = request.GET.get('page')
            try:
                objects = paginator.page(page)
            except PageNotAnInteger:
            
                objects = paginator.page(1)
            except EmptyPage:
            
                objects = paginator.page(paginator.num_pages)
            return render_to_response('contacts.html',{'object_list':objects})
        else:
           print "No contacts"
        return render_to_response( 'contacts.html', {})
    else:
      return render_to_response( 'login.html', {})

@login_required(login_url='/login/')
def addContact(request):
    currentUser = ''
    try:
         currentUser = request.session["user"]
    except :
        print "No session"
    if currentUser:
        loggedInUser = User.objects.get(username = currentUser)
        firstName = request.POST.get('firstName')
        lastName = request.POST.get('lastName')
        email = request.POST.get('email')
        mobile = request.POST.get('mobile')
        alternateNumber = request.POST.get('alternateNumber')
        newContact = contacts()
        newContact.user = loggedInUser
        newContact.firstName = firstName
        newContact.lastName = lastName
        newContact.email = email
        newContact.mobile = mobile
        newContact.alternateNumber = alternateNumber
        newContact.save()
	contactsList = contacts.objects.filter(user=loggedInUser)
        paginator = Paginator(contactsList, 10)
        page = request.GET.get('page')
        '''
        try:
            objects = paginator.page(page)
        except PageNotAnInteger:
            
            objects = paginator.page(1)
        except EmptyPage:
            
            objects = paginator.page(paginator.num_pages)'''
        objects = paginator.page(1)
        return render_to_response('contacts.html',{'object_list':objects,'callbackMessage':"Contact Added Successfully"})
    else:
        return render_to_response( 'login.html', {})

@login_required(login_url='/login/')
def deleteContact(request):
    currentUser = ''
    try:
         currentUser = request.session["user"]
    except :
        print "No session"
    if currentUser:
        loggedInUser = User.objects.get(username = currentUser)
        contact = request.POST.get('contact')
        print contact
        contactToDelete = contacts.objects.filter(id=contact).filter(user=loggedInUser)
        if contactToDelete:
            contactToDelete.delete()
            contactsList = contacts.objects.filter(user=loggedInUser)
            paginator = Paginator(contactsList, 10)
            objects = paginator.page(1)
            return render_to_response('contacts.html',{'object_list':objects,'callbackMessage':"Contact Deleted Successfully"})
        else:
            logout(request)
            return render_to_response( 'login.html', {})
    else:
        return render_to_response( 'login.html', {})

@login_required(login_url='/login/')
def updateContact(request):
    currentUser = ''
    try:
         currentUser = request.session["user"]
    except :
        print "No session"
        return render_to_response( 'login.html', {})
    if currentUser:
        contactId = request.POST.get('contactId')
        loggedInUser = User.objects.get(username = currentUser)
        contactsToEdit = contacts.objects.filter(id=contactId).filter(user=loggedInUser)
        if contactsToEdit:
             
             contactToEdit = contacts.objects.get(id=contactId)
             print contactToEdit
             firstName = request.POST.get('firstName')
             lastName = request.POST.get('lastName')
             email = request.POST.get('email')
             mobile = request.POST.get('mobile')
             alternateNumber = request.POST.get('alternateNumber')
             contactToEdit.firstName = firstName
             contactToEdit.lastName = lastName
             contactToEdit.email = email
             contactToEdit.mobile = mobile
             contactToEdit.alternateNumber = alternateNumber
             contactToEdit.save()
             contactsList = contacts.objects.filter(user=loggedInUser)
             paginator = Paginator(contactsList, 10)
             objects = paginator.page(1)
             return render_to_response('contacts.html',{'object_list':objects,'callbackMessage':"Contact Updated Successfully"})
        else:
             contactsList = contacts.objects.filter(user=loggedInUser)
             paginator = Paginator(contactsList, 10)
             objects = paginator.page(1)
             return render_to_response('contacts.html',{'object_list':objects})
    else:
        return render_to_response( 'login.html',{})
