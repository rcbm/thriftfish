from ext import *

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/dedup', dedup),
                                      ('/search', SearchPage),
                                      ('/scrape', Scrape),
                                      ('/scrape_description', ScrapeDescription),
                                      ('/store', Store),
                                      ('/save', Save),
                                      ('/user', UserPage),
                                      ('/removeEntry', RemoveEntry),
                                      ('/removeFresh', RemoveFresh),
                                      ('/removeQuery', DeleteQuery),
                                      ('/remove_task', Remove_Task),
                                      ('/removefreshemail', RemoveFreshEmail),
                                      ('/email_task', Email_Task),
                                      ('/cron_fetch_handler', CronFetchHandler),
                                      ('/email_handler', EmailHandler),
                                      ('/query_handler', QueryHandler),
                                      ('/scrape_handler', ScrapeHandler),
                                      ('/fetch_query_task', Fetch_Query_Task)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
