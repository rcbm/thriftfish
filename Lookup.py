from simplejson import loads as jsonparse
import urllib2
class Lookup():
    """
    WHEN USER CONNECTS, THIS IS LOADED INTO THE CITY FIELD.  ONE WAY TO MAKE IT MORE ACCURATE IS USE GOOGLE MAPS API TO PINPOINT CLOSEST CL CITY NEAR THEM
    ALTERNATELY WE CAN JUST LEAVE IT W/ THE INPUT CODE AND IF IT DOESNT COME UP WITH ANYTHING, REDIRECT THEM TO A CL CITY LIST
    def get(self, ip):
        geo_url = "http://www.geobytes.com/IpLocator.htm?GetLocation&template=json.txt&IpAddress=127.0.0.1"
        json_stream = urllib2.urlopen(geo_url)
        json_dict = jsonparse(json_stream.read().replace("\r\n",""))['geobytes']
        return json_dict(['city'])
        """
    
    """
    WHEN USER CONNECTS, THIS IS LOADED INTO THE CITY FIELD.  ONE WAY TO MAKE IT MORE ACCURATE IS USE GOOGLE MAPS API TO PINPOINT CLOSEST CL CITY NEAR THEM
    ALTERNATELY WE CAN JUST LEAVE IT W/ THE INPUT CODE AND IF IT DOESNT COME UP WITH ANYTHING, REDIRECT THEM TO A CL CITY LIST
    """
    def get(self, ip):
        geo_url = "http://www.geobytes.com/IpLocator.htm?GetLocation&template=json.txt&IpAddress=%s" % ip
        json_stream = urllib2.urlopen(geo_url)
        json_dict = jsonparse(json_stream.read().replace("\r\n",""))['geobytes']
        return json_dict['city']
    
        #self.response.out.write(json_dict)
        #for e in json_dict:
        #  self.response.out.write(e)
        #self.response.out.write("Country: " + json_dict['country'] + "<br>")
        #self.response.out.write("City: " + json_dict['city'] + "<br>")
        #self.response.out.write("Certainty: " + str(json_dict['certainty']) + "%")
