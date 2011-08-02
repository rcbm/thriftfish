import feedparser
class Search():
    def getResults(self, term, min, max, city):
        # Check to see if the default values of min/max were sent
        # If so, set them to None
        if min == 'Min':
            min = None
        if max == 'Max':
            max = None
            
        term = "+".join("%s" % k for k in term.split(' '))
        new_search = "http://%s.craigslist.org/search/sss?query=%s&srchType=A&minAsk=%s&maxAsk=%s&format=rss" % (city, term, min, max)
        feed = feedparser.parse(new_search)
        results = feed['entries']
        return results
