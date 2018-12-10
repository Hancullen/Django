# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.urls import resolve
from django.test import TestCase
from .views import home, board_topics, new_topic
from .models import Board, Topic, Post

#automated test

class HomeTests(TestCase):
##    def test_home_view_status_code(self):
##        url = reverse('home')
##        response = self.client.get(url)
##        ##if the status code = 200 => success
##        self.assertEquals(response.status_code, 200)
##
##    def test_home_url_resolves_home_view(self):
##    #using resolve function to match a requested URL
##    #with a list of URLs listed in urls.py module
##    #make sure URL '/'(the root of URL), return the home view
##        view = resolve('/')
##        self.assertEquals(view.func, home)

    #create navigation link to the topics page of given Board
    #writing HomeTests firstly
    def setUp(self):
        self.board = Board.objects.create(name='Django', description='Django board.')
        #move 'url' & 'response' here to reuse the same response in new test
        url = reverse('home')
        self.response = self.client.get(url)

    def test_home_view_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_home_url_resolves_home_view(self):
        view = resolve('/')
        self.assertEquals(view.func, home)

    #test the link to the topic page
    def test_home_view_contains_link_to_topics_page(self):
        board_topics_url = reverse('board_topics', kwargs={'pk': self.board.pk})
        #assertContains method tests if the response body
        #has the text href="/boards/1/1"
        self.assertContains(self.response, 'href="{0}"'.format(board_topics_url))



class BoardTopicTest(TestCase):
    #setUp method creates new database which applied all model migrations
    #of current database, run the test and destroys the testing database
    #once its done
    def setUp(self):
        Board.objects.create(name='Ddjango', description='Django board.')

    def test_board_topics_view_success_status_code(self):
        url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    def test_board_topics_view_not_found_status_code(self):
        url = reverse('board_topics', kwargs={'pk':99})
        response = self.client.get(url)
        #code 404, page not found
        self.assertEquals(response.status_code, 404)

    #test if Django is using the correct view function to render
    def test_board_topics_url_resolves_board_topics_view(self):
        view = resolve('/boards/1/')
        self.assertEquals(view.func, board_topics)

    #test the link back to previous page(homepage)
    #same method as test_home_view_contains_link_to_topics_page()
    def test_board_topics_view_contains_link_back_to_homepage(self):
        board_topics_url = reverse('board_topics', kwargs={'pk':1})
        response = self.client.get(board_topics_url)
        homepage_url = reverse('home')
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        self.assertContains(response, 'href="{0}"'.format(homepage_url))
        self.assertContains(response, 'href="{0}"'.format(new_topic_url))


class NewTopicTest(TestCase):
    #creates a Board instance to be used for test                            
    def setUp(self):
        Board.objects.create(name='Django', description='Django board.')
        #create user instance for tests
        User.objects.create_user(username='Han', email='han@gmail.com', password='123')
        
    #check if the request is successful
    def test_new_topic_view_success_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 200)

    #check if the view get 404 error when the Board doesnt exist
    def test_new_topic_view_not_found_status_code(self):
        url = reverse('new_topic', kwargs={'pk': 99})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    #check if the right view is being used
    def test_new_topic_url_resolves_new_topic_view(self):
        view = resolve('/boards/1/new/')
        self.assertEquals(view.func, new_topic)

    #check the link back to list of topics
    def test_new_topic__contains_link_back_to_board_topics_view(self):
        new_topic_url = reverse('new_topic', kwargs={'pk': 1})
        board_topics_url = reverse('board_topics', kwargs={'pk': 1})
        response = self.client.get(new_topic_url)
        self.assertContains(response, 'href="{0}"'.format(board_topics_url))
                                                          
    #make sure HTML contains the token
    def test_csrf(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.get(url)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_topic_valid_post_data(self):
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': 'Test Title',
            'message': 'Oops',
        }
        response = self.client.post(url, data)
        self.assertTrue(Topic.objects.exists())
        self.assertTrue(Post.objects.exists())
        
    #sending an empty dictionary to check how the app is behaving
    def test_new_topic_invalid_post_data(self):
        '''
        Invalid post data should not redirect.
        The expected behavior is to show the form again
        with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        response = self.client.post(url, {})
        self.assertEquals(response.status_code, 200)

    #mostly similar to the above test, but sending some data.
    #App is expected to validate and reject empty subject & message 
    def test_new_topic_invalid_post_data_empty_fields(self):
        '''
        Invalid post data should not redirect.
        The expected behavior is to show the form again
        with validation errors
        '''
        url = reverse('new_topic', kwargs={'pk': 1})
        data = {
            'subject': '',
            'message': '',
        }
        response = self.client.post(url, data)
        self.assertEquals(response.status_code, 200)
        self.assertFalse(Topic.objects.exists())
        self.assertFalse(Post.objects.exists())
        




