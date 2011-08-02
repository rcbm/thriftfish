from google.appengine.api import urlfetch
from google.appengine.api import taskqueue
from google.appengine.ext import webapp
from google.appengine.ext import db
from models import *
from titan.BeautifulSoup import *
import re
import hashlib

class dedup(webapp.RequestHandler):
    def get(self):
        rows = db.GqlQuery("SELECT link FROM Entry WHERE page_hash = null limit 10")
        for row in rows:
            print hashlib.md5(row.link).hexdigest()
    
			
'''
class Parse(webapp.RequestHandler):
    def tokenize(self, text):
        """ break up some abritrary text into tokens """
        # get rid of all punctuation
        rex = re.compile(r"[^\w\s]")
        text = rex.sub('', text)

        # create NLTK objects we'll need
        stemmer = PorterStemmer()
        tokenizer = WhitespaceTokenizer()

        # break text up into words
        tokens = tokenizer.tokenize(text)

        # get the stems of the words
        words = [stemmer.stem(token.lower()) for token in tokens]

        return words
    
    def get(self):
        q = Entry.all()
        i = 0
        
        fd = FreqDist()
        for e in q:
            i += 1
            words = self.tokenize(e.title)
            for word in words:
                fd.inc(word)

        for k in fd.keys():
            self.response.out.write(str(k) + ": " + str(fd[k]) + "<BR>")
'''

class ScrapeHandler(webapp.RequestHandler):
    def get(self):
        city = 'losangeles'
        count = 0
        #maxcount = 3400       # a four digit number, ie xxx,x00
        maxcount = 1
        self.response.out.write("<h2>Total listings to be fetched: %s * 100 = %s<BR></h2>" % (maxcount, maxcount*100))
        while count < maxcount:
            fetchurl = "http://%s.craigslist.org/sss/index%s00.html" % (city, count)
            taskqueue.add(url="/scrape", params={ 'url':fetchurl })
            count += 1

'''
GQL BY DATE:
SELECT * FROM Entry
WHERE date < DATETIME(2011, 7, 25, 12, 00, 00)
'''

class Scrape(webapp.RequestHandler):
    def post(self):
        rpc = urlfetch.create_rpc(10)
        fetch = urlfetch.make_fetch_call(rpc, self.request.get('url'))
        try:
            result = rpc.get_result()
            if result.status_code == 200:
                results = result.content
                p = SoupStrainer('p')
                listings = [tag for tag in BeautifulSoup(results, parseOnlyThese=p)]
                entries = []
                for index, l in enumerate(listings):
                    if index != len(listings) - 1 and l.findAll('a')[1]['href'] != "/wan/":
                        '''
                        price = l.contents[4]
                        url = l.contents[3]['href']
                        title = l.contents[3].contents[0]
                        location = l.contents[5]
                        self.response.out.write(str(l.contents[3].contents[0]) + "<BR>")
                        self.response.out.write("Price: " + str(l.contents[4].strip("- ")) + "<BR>")
                        self.response.out.write(str(l.contents[3]['href']) + "<BR><br>")
                        '''
                        entries.append(Entry(price = str(l.contents[4].strip("- \n\t ")), title = str(l.contents[3].contents[0]), link = str(l.contents[3]['href'])))
                try:
                    for entry in entries:
                        db.put(entry)
                        taskqueue.add(url="/scrape_description", params={ 'key':entry.key() })
                except: pass
        except: pass
            
class ScrapeDescription(webapp.RequestHandler):
    # get a key, pull the url, go to the url and store the result, hash the result, save the entity
    def post(self):
        q = db.get(self.request.get('key'))
        rpc = urlfetch.create_rpc(10)
        fetch = urlfetch.make_fetch_call(rpc, q.link)
        try:
            results = rpc.get_result()
            if results.status_code == 200:
                try:
                    q.description = results
                    q.page_hash = hashlib.md5(results).hexdigest()
                    db.put(q)
                except Exception: pass
                #except Exception, er:
                #    print 'SCRAPE ERROR: %s' %er
        except Exception: pass
        #except Exception, er:
        #    print 'SCRAPE ERROR: %s' %er
            
