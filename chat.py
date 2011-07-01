# -*- coding: utf-8 -*-

import cgi
import uuid
import os
import logging

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import channel, memcache, users

from django.utils import simplejson as json



class MemcacheList(object):

    def __init__(self, key):
        self.memcache_key = key

    def __call__(self):
        items = memcache.get(self.memcache_key) 
        return items if items else []

    def __iter__(self):
        return self()

    def insert(self, i, x):
        items = self()
        ret = items.insert(i, x)
        while len(items):
            try:
                memcache.set(self.memcache_key, items)
            except ValueError:  # over size limit(1000KB, not equal 'KiB')
                items.pop()
            else:
                break
        return ret

    def append(self, x):
        self.insert(0, x)

    def remove(self, x):
        items = self()
        ret = items.remove(x)
        memcache.set(self.memcache_key, items)
        return ret

    def pop(self, i=None):
        items = self()
        ret = items.pop() if i is None else items.pop(i)
        memcache.set(self.memcache_key, items)
        return ret

    def index(self, x):
        items = self()
        return items.index(x)

    def count(self, x):
        items = self()
        return items.count(x)

    def sort(self):
        items = self()
        items.sort()
        memcache.set(self.memcache_key, items)

    def reverse(self):
        items = self()
        items.reverse()
        memcache.set(self.memcache_key, items)


MAX_LENGTH = 1000


members = MemcacheList('members')
messages = MemcacheList('messages')


def deliver_message(mes):
    """Deliver the message to all logged-in members."""
    formatted_mes = '%s\n\n' % mes[:MAX_LENGTH]
    messages.append(formatted_mes)
    for client_id in members():
        channel.send_message(client_id, formatted_mes)


# login required by app.yaml

class IndexHandler(webapp.RequestHandler):

    def get(self):
        user = users.get_current_user()
        values = {
            'token': channel.create_channel(user.nickname()),
            'nickname': user.nickname()
        }

        logging.info('request by %s' % values['nickname'])

        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, values))



class ConnectedHandler(webapp.RequestHandler):
    """Call post method when connected to channel from the user."""

    def post(self):
        client_id = self.request.get('from', default_value=None)

        logging.info('connect: %s' % client_id)

        if client_id:
            members.append(client_id)
            deliver_message(u'%s has joined!' % client_id)

    def get(self):
        logging.info('get!!')


class DisconnectedHandler(webapp.RequestHandler):
    """Call post method when disconnected the user from channel."""

    def post(self):
        client_id = self.request.get('from')

        logging.info('disconnect: %s' % client_id)

        members.remove(client_id)
        deliver_message(u'%s has left.' % client_id)



class MessageHandler(webapp.RequestHandler):
    """Message from any users."""
    
    def post(self):
        """Post the message,
        and deliver one to all users.
        """
        mes = self.request.get('mes', default_value=None)
        if mes is None:
            return
        user = users.get_current_user()
        deliver_message(u'%s:\n%s' % (user.nickname(), mes))

    def get(self):
        """Get message log."""
        self.response.out.write(json.dumps(messages()))


