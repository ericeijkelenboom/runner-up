import cgi
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
import logging
from google.appengine.ext.webapp import template
from models import FoodItem
from models import Route
from models import Vertex
from django.utils import simplejson

class MainPage(webapp.RequestHandler):
  def get(self):
    fooditems = FoodItem.all().fetch(15);
    template_values = { 'fooditems': fooditems }

    path = os.path.join(os.path.dirname(__file__), 'main.html')
    self.response.out.write(template.render(path, template_values))

class FoodUpdater(webapp.RequestHandler):
    def get(self):
        fooditems = FoodItem.all().fetch(15)
        template_values = { 'fooditems': fooditems }
        
        path = os.path.join(os.path.dirname(__file__), 'foodupdater.html')
        self.response.out.write(template.render(path, template_values))
        
    def post(self):
        if(cgi.escape(self.request.get('action')) == 'add'):
            fooditem = FoodItem()
            fooditem.name = cgi.escape(self.request.get('fooditem_name'))
            fooditem.kcals = int(cgi.escape(self.request.get('fooditem_kcals')))
            fooditem.put()
        
        # Implement delete
        
        self.redirect('/foodupdater')
        
class RouteManager(webapp.RequestHandler):        
    def post(self):
      if(self.request.get('action') == 'save'):
        routename = self.request.get('name')
        
        routes = Route.gql("WHERE name = :1", routename).fetch(1)
        if len(routes) > 0:
            self.response.out.write('Route %s already exists.' % routename)
            return
            
        json_route = simplejson.loads(self.request.get('route'))
        logging.info('JSON route = %s', json_route)
        
        vertices = [latLng.split(',') for latLng in json_route]
        
        route = Route()
        route.name = routename
        route.put()
        
        logging.info('Inserted route with name %s and id %s', route.name, route.key())
        
        for index in range(0, len(vertices)):
            vertex = Vertex()
            vertex.lat = float(str(vertices[index][0]))
            vertex.lng = float(str(vertices[index][1]))
            vertex.route = route
            vertex.put()
            logging.info('Inserted vertex %s, %s on route %s with id %s', vertex.lat, vertex.lng, vertex.route.name, vertex.key())
        
        self.response.out.write('Success')

    def get(self):
      action = cgi.escape(self.request.get('action'))
      logging.info('RouteManager - GET. Action parameter: %s', action)
      
      if(action == 'load'):
        routename = cgi.escape(self.request.get('routename'))
        error_msg = ''
        
        routes = Route.gql("WHERE name = :1", routename).fetch(1)
        
        if(len(routes) == 0):
          error_msg = "No route with name %s" % routename
        
        route = routes[0];
        
        logging.info('Loading route %s', route.name)
        
        vertices = []
        for vertex in route.vertex_set:
          vertices.append({'lat': vertex.lat, 'lng': vertex.lng})
          logging.info('Loaded vertex with lat %s and lng %s', vertex.lat, vertex.lng)
        
        result = {'error': error_msg, 'vertices': vertices, 'routename': routename };
        
        #result = { 'vertices': vertices, 'error_msg': error_msg }
        #template_values = { 'result': result }
        #path = os.path.join(os.path.dirname(__file__), 'buildroute.html')
        #self.response.out.write(template.render(path, template_values))
        
        self.response.out.write(simplejson.dumps(result))
      
      elif action == 'allnames':
        logging.info('YEAH BITCH!')
        
        result = []
        
        routes = Route.all()
        
        logging.info("Routes %s", routes);
        for route in routes:
          logging.info('Found route name %s', route.name);
          result.append(route.name)
      
        self.response.out.write(simplejson.dumps(result))
        
        
        