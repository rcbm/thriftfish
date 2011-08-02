import datetime
from formatDatetime import *
from Search import *
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
from models import *
from google.appengine.api import taskqueue

class QueryHandler(webapp.RequestHandler):
    def post(self):
        user = db.get(self.request.get('key'))
        for query_key in user.queries:
            taskqueue.add(url="/fetch_query_task", params={'key': query_key})

class Fetch_Query_Task(webapp.RequestHandler):
    def post(self):
        """
        This receives a Query Object and performs a Search based on information from that Query.

        It then compares the results to the search_date and if they are deemed fresh, stores them.
        """
        
        new_search = Search()
        f = formatDatetime()

        q = db.get(self.request.get('key'))
        results = new_search.getResults(q.term, q.min, q.max, q.city)
        
        # Pull fresh listings from query, if they exist
        if q.fresh:
            fresh = q.fresh
        else: 
            fresh = FreshEntries()
            fresh.entries = [] # Store fresh listings here

        search_date = q.search_date
        latest_entry_time = search_date

        # Compare each entry datetime to the saved datetime
        for e in results:
            # Extract and format times from feed
            f_entry_time = f.craigslist_to_datetime(e.date)

            # Compute elapsed time since last search and this listing
            difference = f_entry_time - search_date

            # If entry is after the saved time, flag it as fresh
            if f_entry_time > search_date:

                # Check and see if this is the chronologically latest listing
                if f.craigslist_to_datetime(e.date) > latest_entry_time:
                    latest_entry_time = f.craigslist_to_datetime(e.date)

                entry = Entry(date = e.date, title = e.title, link = e.link)
                db.put(entry)
                fresh.entries.append(entry.key())
        db.put(fresh)

        # put back query with new search_date and new fresh listings
        q.search_date = latest_entry_time
        q.fresh = fresh
        db.put(q)

class CronFetchHandler(webapp.RequestHandler):
    def get(self):
        users = User.all()
        for u in users:
            user_key = u.key()
            taskqueue.add(url="/query_handler", params={'key': user_key})

