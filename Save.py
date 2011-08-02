import datetime
from google.appengine.ext import db
from google.appengine.api import users
from google.appengine.ext import webapp
from formatDatetime import *
from models import *

class Save(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            f = formatDatetime()
            current_user = users.get_current_user()
            old_user = db.GqlQuery("SELECT * FROM User WHERE user_id = '%s'" % current_user.user_id()).get()
            term = self.request.get('term')
            min = self.request.get('Min')
            max = self.request.get('Max')
            city = self.request.get('City')
            search_date = self.request.get('Search_Date')
            if search_date:
                search_date = f.string_to_datetime(search_date)
            else:
                search_date = datetime.now()
                
            if old_user:
                found_existing_query = False
                for q in old_user.queries:
                    if db.get(q).term.lower() == term.lower() and db.get(q).city.lower() == city.lower():
                        found_existing_query = True

                if found_existing_query:
                    self.response.out.write("Sorry-- It looks like you've already searched for this so, we won't save this one again<br>")
                else:
                    # Save to the datastore
                    query = Query(author = current_user, search_date = search_date, term = term, min = min, max = max, city = city)
                    query.put()
                    old_user.queries.append(query.key())
                    old_user.put()
                    self.redirect("/user")
            else:
                query = Query(author = users.get_current_user(), search_date = search_date, term = term, min = min, max = max, city = city)
                query.put()
                
                current_user = users.get_current_user()
                user_profile = User(user = current_user, user_id = current_user.user_id(), email = current_user.email())
                user_profile.queries = [query.key()]
                user_profile.put()
                self.redirect("/user")
        else:
            self.redirect(users.create_login_url(self.request.uri))
