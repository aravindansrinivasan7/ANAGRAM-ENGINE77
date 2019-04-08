from itertools import groupby
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import DATASTORE
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        my_list = None
        user = users.get_current_user()
        uq=0
        st=0
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'LOGOUT'
            key = ndb.Key('DATASTORE', user.user_id())
            my_list = key.get()
            user=users.get_current_user().email()
            query=DATASTORE.query(DATASTORE.email==users.get_current_user().email())
            for i in query:
                uq=uq+1
            for i in query:
                for j in i.strings:
                    st=st+1
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'LOGIN'


        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'my_list' : my_list,'uq':uq,'st':st}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            strw = self.request.get('input')
            strw77=''.join(k for k, g in groupby(sorted(strw)))
            keys_email=users.get_current_user().email()
            q = DATASTORE.query(DATASTORE.email == keys_email)
            for i in q:
                    if strw in i.strings:
                        self.redirect('/exist')
                        return
            action=self.request.get('button')
            if action == 'ADD':
                key = ndb.Key('DATASTORE', strw77+keys_email)
                my_list = key.get()
                if my_list==None:
                    my_list=DATASTORE(id=strw77+keys_email)
                    my_list.put()
                key = ndb.Key('DATASTORE', strw77+keys_email)
                my_list = key.get()
                strw = self.request.get('input')
                if strw == None or strw == '':
                    self.redirect('/')
                    return
                my_list.strings.append(strw)
                my_list.lexographical=strw77
                my_list.wordcount=len(my_list.strings)
                my_list.lettercount=len(my_list.lexographical)
                my_list.email=keys_email
            my_list.put()
            self.redirect('/newword')

class AddPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('newword.html')
        self.response.write(template.render(template_values))

class SearchA(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        email=users.get_current_user().email()
        strw = self.request.get('input77')
        strw77=''.join(k for k, g in groupby(sorted(strw)))
        action=self.request.get('button')
        de,z,m,s=[],0,[],0
        if action == 'SEARCH':
            if strw77==None or '':
                pass
            else:
                c=[]
                query=DATASTORE.query(DATASTORE.email==users.get_current_user().email())
                for i in query:
                    for j in i.lexographical:
                        if j in strw77:
                            c.append(i.lexographical)
                        else:
                            break
                            break
                for i in query:
                    z=len(i.lexographical)
                    s=c.count(i.lexographical)
                    if z==s:
                        m.append(i.lexographical)
                    else:
                        pass
                if strw77 in m:
                    m.remove(strw77)
                for i in m:
                    key1=ndb.Key('DATASTORE',i+email)
                    my_list1=key1.get()
                    de.append(my_list1)
        key = ndb.Key('DATASTORE', strw77+email)
        my_list = key.get()
        template_values = {'my_list':my_list,'de':de}
        template = JINJA_ENVIRONMENT.get_template('sub.html')
        self.response.write(template.render(template_values))

class UNIQUE(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user().email()
        query=DATASTORE.query(DATASTORE.email==users.get_current_user().email())
        a=0
        for i in query:
            a=a+1
        template_values = {'query':query,'a':a}
        template = JINJA_ENVIRONMENT.get_template('unique.html')
        self.response.write(template.render(template_values))

class WordList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('wordlist.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user().email()
        textfile = self.request.get("myFile")
        textfile = textfile.split()
        for x in textfile:
            line=''.join(k for k, g in groupby(sorted(x)))
            key = ndb.Key('DATASTORE', line+user)
            my_list = key.get()
            if my_list==None:
                my_list=DATASTORE(id=line+user)
                my_list.put()
            keys_email=users.get_current_user().email()
            key = ndb.Key('DATASTORE', line+user)
            my_list = key.get()
            if x in my_list.strings:
                pass
            else:
                my_list.strings.append(x)
                my_list.lexographical=line
                my_list.wordcount=len(my_list.strings)
                my_list.lettercount=len(my_list.lexographical)
                my_list.email=user
                my_list.put()
        self.redirect('/')

class EXIST(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<h1><center>SORRY, GIVEN WORD ALREADY EXIST IN DATASTORE""")
        self.response.out.write("<b><p><a href='/newword'>TRY AGAIN</a></p></b>")
        self.response.out.write("<b><p><a href='/'>HOME</a></p></b>")
        self.response.out.write("</body></html>")

class ANAGRAM(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user().email()
        my_list=''
        strw = self.request.get('input')
        strw77=''.join(k for k, g in groupby(sorted(strw)))
        action=self.request.get('button')
        if action=="SEARCH":
            key = ndb.Key('DATASTORE', strw77+user)
            my_list = key.get()
        template_values = {'my_list':my_list}
        template = JINJA_ENVIRONMENT.get_template('anagram.html')
        self.response.write(template.render(template_values))





app = webapp2.WSGIApplication([('/', MainPage),('/newword',AddPage),('/sub',SearchA),('/unique',UNIQUE),('/wordlist',WordList),('/exist',EXIST),('/anagram',ANAGRAM)], debug=True)
