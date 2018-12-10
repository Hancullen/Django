# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User

#Views are Python functions that receive an HttpRequest object
#and return HttpResponse object.

from django.http import HttpResponse
from .models import Board, Topic, Post
from django.http import Http404
from .forms import NewTopicForm

def home(request):
    boards = Board.objects.all()
    boards_names = list()
    #already declared in python shell:
    #board = Board(name='Django', description='...')
    #board = Board(name='Python', descrition='...')

##    for board in boards:
##        boards_names.append(board.name)
##
##    response_html = '<br>'.join(boards_names)
    
##    return HttpResponse(response_html)
    return render(request, 'home.html', {'boards': boards})

def about(request):
    return render(request, 'about.html')

#keyword argument 'pk' must be matched with url pattern(?P<pk>\d+)
#'pk' = Primary Key
def board_topics(request, pk):
    try:
        board = Board.objects.get(pk=pk)
    except Board.DoesNotExist:
        raise Http404
    board = get_object_or_404(Board, pk=pk)
    return render(request, 'topics.html', {'board': board})
    
##def about_company(request):
##    return render(request, 'about_company.html', {'board': board})

def new_topic(request, pk):
    board = get_object_or_404(Board, pk=pk)
    user = User.objects.first() #get the currently logged in user

    #check if request is POST or GET
    if request.method == 'POST': #user is submitting data to server
        #passing the POST data to the form
        form = NewTopicForm(request.POST)
        #ask Django to verify data
        if form.is_valid():
            topic = form.save(commit=False)
            topic.board = board
            topic.starter = user
            topic.save() #save data to the database
            post = Post.objects.create(
                message =  form.cleaned_data.get('message'),
                topic = topic,
                created_by = user
            )

            #redirect to the created topic page
            return redirect('board_topics', pk = board.pk)
    else: #if request is a GET, initialize a new and empty form
        form = NewTopicForm()
    #have to update the new_topic.html to display errors properly   
    return render(request, 'new_topic.html', {'board': board, 'form': form})

##        subject = request.POST['subject']
##        message = request.POST['message']
##        
##        #get the currently login user
##        user = User.objects.first() 
##
##        #start a new topic
##        topic = Topic.objects.create(
##            subject = subject,
##            board = board, #this is ForeignKey(Board)
##            starter = user
##            )
##
##        #receive data from HTML
##        post = Post.objects.create(
##            message = message,
##            topic = topic,
##            created_by = user
##            )
##
            

    
