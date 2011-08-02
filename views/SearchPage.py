import os
from formatDatetime import *
from google.appengine.ext.webapp import template
from google.appengine.api import users
from google.appengine.ext import webapp
from Search import *

class SearchPage(webapp.RequestHandler):
    def get(self):
            
        if users.get_current_user():
            url = "/user"
            url_linktext = 'My Want List'
        else:
            url = users.create_login_url(self.request.uri)
            url_linktext = 'Login'

        f = formatDatetime()

        formatted_term = self.request.get('q')

        # handle spaces in query terms
        min = self.request.get('Min')
        max = self.request.get('Max')
        city = self.request.get('City')
        new_search = Search()
        try:
            results = new_search.getResults(formatted_term, min, max, city)
            if results:
                search_date = f.craigslist_to_datetime(results[0].date)
            else:
                search_date = datetime.now()

            template_values = {
                'search_date': search_date,
                'term': formatted_term,
                'min': min,
                'max': max,
                'city': city,
                'results': results,
                'url': url,
                'url_linktext': url_linktext,
                }
            path = os.path.join(os.path.dirname(__file__), '../static/html/search.html')
            self.response.out.write(template.render(path, template_values))
        except:
            self.response.out.write("Sorry, there was an error connecting to Craigslist.  Try checking your 'City' field, or possibly your internet connection, and try again.")

