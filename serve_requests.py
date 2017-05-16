import cherrypy
import sc
import json
import os
from jinja2 import Environment, FileSystemLoader


env = Environment(loader=FileSystemLoader('templates'))
#Jinja2 template engine was used to render the html page



class scraping_nifty(object):

    @cherrypy.expose()

    def index(self):

         return open(os.path.join('view','home.html'))


    @cherrypy.expose()

    def redirection_to(self):

         return file(os.path.join('view','card_layout.html'))





    @cherrypy.expose()

    def scrape_for_values_gainers(self):
        sc.fetch_and_store()
        ga,lo=sc.retrive_and_display()
        ga_json=json.dumps(ga)
        lo_json=json.dumps(lo)




        tmpl = env.get_template('cards_display.html')
#the template is cards_display.html which gets loaded into the frontend. this template generates cards for both loosers and gainers
        return tmpl.render(gainers=ga,loosers=lo)




cherrypy.config.update({'server.socket_host': '127.0.0.1',
                         'server.socket_port': 8080, })


cherrypy.quickstart(scraping_nifty())
