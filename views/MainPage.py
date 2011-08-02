import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

class MainPage(webapp.RequestHandler):
    def get(self):
        try:
            l = Lookup()
            city = l.get(self.request.remote_addr)
        except:
            city = 'Pittsburgh'

        url = "/user"
        if users.get_current_user():
            url_linktext = 'My Want List'
        else:
            url_linktext = 'Login'

        template_values = {
            'city': city,
            'url': url,
            'url_linktext': url_linktext,
            }
            
        path = os.path.join(os.path.dirname(__file__), '../static/html/index.html')
        #path = 'index.html'
        self.response.out.write(template.render(path, template_values))

