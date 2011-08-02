from ext import *
from titan.bottlenose import api
from titan.config import *
from titan.BeautifulSoup import *
from titan.amazonproduct import *

class MainPage(webapp.RequestHandler):
    def get(self):
        template_values = {
            #'city': city,
            #'login_url': url,
            #'url_linktext': url_linktext,
            }
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))

        path = os.path.join(os.path.dirname(__file__), 'search_box.html')
        self.response.out.write(template.render(path, {}))
        
class SearchPage(webapp.RequestHandler):
    def get(self):
        """
        Schema:
        prices = [ offer1, offer2, offer3, ... ]
        offer = { new : { formatted, unformatted }, used: { formatted, unformatted } }
        """

        query = self.request.get('q')
        
        #api = API(AWS_KEY, SECRET_KEY, 'us')
        #search = api.item_search(search_index='All', Keywords=query)
        #soup = BeautifulStoneSoup(str(search))

        #price = api.item_search(search_index='All', Keywords=query, ResponseGroup='OfferSummary')
        #price_soup = BeautifulStoneSoup(str(price))

        #self.response.out.write(str(price_soup.prettify()))

        '''
        Possibly Use Medium Response group to combine
        '''

        
        amazon = api.Amazon(AWS_KEY, SECRET_KEY)
        response = amazon.ItemSearch(SearchIndex='All', Keywords=query, ResponseGroup = "OfferSummary")
        search = amazon.ItemSearch(SearchIndex='All', Keywords=query)
        soup = BeautifulStoneSoup(search)
        
        #response = amazon.ItemSearch(SearchIndex='All', Keywords=query, Style="http://xml2json-xslt.googlecode.com/svn/trunk/xml2json.xslt")
        '''
        response = amazon.ItemLookup(ItemId = query, ResponseGroup =
                                     "OfferSummary", SearchIndex = "Books", IdType = "ISBN",
                                     Style="http://xml2json-xslt.googlecode.com/svn/trunk/xml2json.xslt")
        '''

        price_soup = BeautifulStoneSoup(response)
        #self.response.out.write(soup.prettify())
        
        #self.response.out.write(response)
        #test = api.item_search(search_index='All', Keywords=query, ResponseGroup='OfferFull')
        #test_soup = BeautifulStoneSoup(str(test))
        #self.response.out.write(str(test_soup.prettify()))
        
        





        # Use this to make an array of prices
        offers = []
        for item in price_soup.findAll('item'):
            for o in item.findAll('offersummary'):

                if o.find('lowestnewprice'):
                    new =  {'unformatted' : str(o.find('lowestnewprice').find('amount')).strip('<amount>').strip('</amount>'),
                    'formatted' :  str(o.find('lowestnewprice').find('formattedprice')).strip('<formattedprice>').strip('</formattedprice>')}
                else:
                    new = None
                    
                if o.find('lowestusedprice'):
                    used = {'unformatted' : str(o.find('lowestusedprice').find('amount')).strip('<amount>').strip('</amount>'),
                    'formatted' : str(o.find('lowestusedprice').find('formattedprice')).strip('<formattedprice>').strip('</formattedprice>')}
                else:
                    used = None
                    
                offer = {'new': new, 'used':used}
                offers.append(offer)

        #self.response.out.write(offers[3]['new']['formatted'])


        # Use this to make an array of items
        results = []
        for item in soup.findAll('item'):
            url = str(item.contents[1]).strip('<detailpageurl>')
            asin = str(item.contents[0]).strip('<asin>')
            title = str(item.contents[3].find('title').contents[0]).strip()
            
            result = [url, title, asin]
            results.append(result)
            self.response.out.write('</a></div>')
        
        # Iterate through both arrays using zip() - fingers crossed, they should sync up
        item_pairs = zip(results, offers)
        
        '''
        # Iterate through both arrays using zip() - fingers crossed, they should sync up
        for q, o in zip(results, offers):
            self.response.out.write(q[1])
            self.response.out.write("<BR>")
            for k, v in o.iteritems():
                if v:
                    self.response.out.write(str(k) + ": " + str(v['formatted']) + "<BR>")
            self.response.out.write("<BR>")
        '''
            
            
        
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, {}))

        path = os.path.join(os.path.dirname(__file__), 'search.html')
        self.response.out.write(template.render(path, {'item_pairs': item_pairs}))

        path = os.path.join(os.path.dirname(__file__), 'search_box.html')
        self.response.out.write(template.render(path, {}))
        
        
            
application = webapp.WSGIApplication([('/titan', MainPage),
                                     ('/titan/', MainPage),
                                     ('/titan/search', SearchPage)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
