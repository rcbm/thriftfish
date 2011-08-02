import cgi
from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext import db
import os
from google.appengine.ext.webapp import template

class UserPage(webapp.RequestHandler):
    def get(self):
        if users.get_current_user():
            logged_in = True
            url = users.create_logout_url("/")
            url_linktext = 'Logout'

            old_user = db.GqlQuery("SELECT * FROM User WHERE user_id = '%s'" % users.get_current_user().user_id()).get()
            if old_user:
                queries_keys = old_user.queries
            else:
                queries_keys = []
                
            querylist = []
            if len(queries_keys) > 0:
                for e in queries_keys:
                    q = db.get(e)
                    header = [q.key()]           # First Item in Query is its own key

                    # Prettify the Ranges of Search Queries
                    if not q.min:
                        q.min = None;
                    if not q.max:
                        q.max = None;

                    if q.min == "Min" or q.min == "None" or q.min == None or q.min == "0":
                        if q.max == "Max" or q.max == "None" or q.max == None or q.max == "0":
                            header.append("You searched for <b>'%s'</b>" % q.term)
                        else:
                            header.append("You searched for <b>'%s'</b> up to <b>$%s</b>" % (q.term, q.max))
                    else:
                        if q.max == "Max" or q.max == "None" or q.max == None or q.max == "0":
                            header.append("You searched for <b>'%s'</b> from <b>$%s</b>" % (q.term, q.min))
                        else:
                            header.append("You searched for <b>'%s'</b> from <b>$%s</b> to <b>$%s</b>" % (q.term, q.min, q.max)) 
                    header.append(q.city)
                        
                    listings = []
                    if q.fresh:                              # if fresh results
                        header.append(q.fresh.key())                  # append fresh listings key to header at position q.2
                        for e in q.fresh.entries:                     # iterate through entries in fresh
                            entry = []                                # set up dictionary
                            key = str(e) 
                            e = db.get(key)                           # retrieve entry object
                            if e:
                                entry.append(key)                     # first term in any entry list is its own key
                                entry.append(q.fresh.key())           # second term in any entry list is the parent's key
                                entry.append(e)                       # append entry at [1]
                            listings.append(entry)                    # add entry to fresh listings
                        header.append(listings)
                        
                    querylist.append(header)
                
            template_values = {
                'querylist': querylist,
                'logged_in': logged_in,
                'url': url,
                'url_linktext': url_linktext,
            }

            path = os.path.join(os.path.dirname(__file__), '../static/html/user.html')
            self.response.out.write(template.render(path, template_values))

            """
            TO-CLIENT LIST ORGANIZATION:

            query = [ ['self_key', 'results_html', city, 'listings_key', listings] ] 
            listings = [entry_1, entry_2, entry_3]
            entry = ['self_key', 'parent_key', e-object]

            """

        else:
            self.redirect(users.create_login_url(self.request.uri))
        
