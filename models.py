from google.appengine.ext import db

class Entry(db.Model):
    date = db.StringProperty()
    link = db.StringProperty()
    title = db.StringProperty(multiline=True)
    price = db.StringProperty()
    description = db.TextProperty()
    page_hash = db.StringProperty()
    
class FreshEntries(db.Model):
    entries = db.ListProperty(db.Key)

class Query(db.Model):
    author = db.UserProperty()
    term = db.StringProperty()
    min = db.StringProperty()
    max = db.StringProperty()
    city = db.StringProperty()
    bookmarked_listings = db.ListProperty(int)
    search_date = db.DateTimeProperty()
    fresh = db.ReferenceProperty(FreshEntries)
    
class User(db.Model):
    user = db.UserProperty(required=True)
    user_id = db.StringProperty(required=True)
    email = db.EmailProperty()
    queries = db.ListProperty(db.Key)


    
"""
    Query
     - FreshEntries
        -- Entry
            --- title, date, link

            
grab listings page
           save all titles, links, prices, links
                click on each entry, save plaintext file for processing later
                click on 'next 100' listing - maybe do this manually? 
                               "index%s00.html" % count
title
link
"""

