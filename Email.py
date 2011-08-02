from google.appengine.ext import webapp
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.api import mail
from models import *
from google.appengine.api import taskqueue

class EmailHandler(webapp.RequestHandler):
    def get(self):
        users = User.all()
        for u in users:
            user_key = u.key()
            taskqueue.add(url="/email_task", params={'key': user_key})
            
                
class Email_Task(webapp.RequestHandler):
    def post(self):
        user_key = self.request.get('key')
        user = db.get(user_key)
        fresh_results = False       # Use this to track if there are any fresh results at all

        email = '' # Use this to compose a new email w/ results
        header = "<html><body><h2>List of all Fresh Entries: </h2>"
        header += "<a href='http://my-want-list.appspot.com/removefreshemail?key=%s'><b>(Remove All Fresh Results)</b></a><br><BR>" % (user_key)
        email += header


        for query_key in user.queries:
            q = db.get(query_key)
            fresh = FreshEntries()

            if q.fresh and len(q.fresh.entries) > 0:
                fresh_results = True
                subheader = "Search term: <b>'%s'</b> with min: <b>%s</b> and max: <b>%s</b>" % (q.term, q.min, q.max) + "<br><br>"
                email += subheader
                fresh.entries = q.fresh.entries
                fresh_count = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;There are <b>" + str(len(q.fresh.entries)) + "</b> fresh: <br>"
                email += fresh_count
                for e in q.fresh.entries:
                    e = db.get(e)
                    spacing = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
                    listing = spacing + "<a href='" + e.link + "'>" + e.title + "</a><br>"
                    email += listing
                email += "<br>"

        if fresh_results:
            # There must be something to send then, so proceed
            message = mail.EmailMessage()
            message.sender = 'info@thriftfish.com'
            message.subject = "Your Fresh Listings await!"
            message.to = user.email
            message.body = '&nbsp;'
            message.html = "<html><META HTTP-EQUIV='Content-Type' CONTENT='text/html'><head></head><body>" + email + "</body></html>" 
            #message.html = template.render('mail.html', template_values))
            message.send()
