from google.appengine.ext import webapp
class Store(webapp.RequestHandler):
    """
    USE THIS TO BOOKMARK A LISTING
    EVENTUALLY IMPLIMENT JQUERY TO JUST HIDE THAT PARTICULAR DOM ELEMENT
    """
    def get(self):
        f = formatDatetime()
        query = Query()
        queries = Query.all()
        if users.get_current_user():
            query.author = users.get_current_user()

        query.term = self.request.get('term')
        query.min = self.request.get('Min')
        query.max = self.request.get('Max')
        query.search_date = f.string_to_datetime(self.request.get('Search_Date'))
        
        bookmarks = []
        a = urlsplit(self.request.get('listing'))
        bookmarks.append(int(basename(a[2]).split('.')[0]))
        query.bookmarked_listings = bookmarks
            
        query.put()
        self.redirect('/fetch')
        #self.redirect('/search?q=' + query.term + "&Min=" + query.min + "&Max=" +query.max)
