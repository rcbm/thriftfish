from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.api import taskqueue
from google.appengine.api import users

# DB Remove handlers and task
class DeleteQuery(webapp.RequestHandler):
    def post(self):
        user = users.get_current_user()
        query = db.get(self.request.get('q'))

        if query.fresh:
            if len(query.fresh.entries) > 0:
                for e in query.fresh.entries:
                    taskqueue.add(url="/remove_task", params={'key': e})
        
            taskqueue.add(url="/remove_task", params={'key': query.fresh.key()})

        taskqueue.add(url="/remove_task", params={'key': query.key()})
        
        old_user = db.GqlQuery("SELECT * FROM User WHERE user_id = '%s'" % user.user_id()).get()
        old_user.queries.remove(query.key())
        old_user.put()
        
class RemoveEntry(webapp.RequestHandler):
    # Used to delete a key when a parent key has been provided
    def post(self):
        ekey = self.request.get('q')
        parent = db.get(self.request.get('p'))
        parent.entries.remove(db.Key(ekey))
        parent.put()
        taskqueue.add(url="/remove_task", params={'key': ekey})

class RemoveFreshEmail(webapp.RequestHandler):
    # Used to delete all fresh listings when request is received via ajax-request w/ key in email
    def get(self):
        user = db.get(self.request.get('key'))    # get user_key from client, look up in DB
        for e in user.queries:                    # for each element in user.queries
            query = db.get(e)
            for q in query.fresh.entries:
                taskqueue.add(url="/remove_task", params={'key': q})
            del query.fresh.entries[:]
            query.fresh.put()
        self.redirect("/user")              # Possibly redirect user to home page ? 
        
class Remove_Task(webapp.RequestHandler):
    def post(self):
        db.delete(self.request.get('key'))
        
class RemoveFresh(webapp.RequestHandler):
    # Used to delete a key when a parent key has been provided
    def post(self):
        fkey = self.request.get('q')     # get key from client
        fresh = db.get(fkey)             # use key to lookup fresh entity
        for e in fresh.entries:          # loop through list and delete each entity by key
            taskqueue.add(url="/remove_task", params={'key': e})
            
        del fresh.entries[:]             # empty out fresh.entries list
        fresh.put()                      # save empty fresh.entries back to datastore
        self.redirect("/user")
        
