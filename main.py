from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
import os
import views

def main():
  application = webapp.WSGIApplication( [('/', views.MainPage),
                                         ('/foodupdater', views.FoodUpdater),
                                         ('/routemanager', views.RouteManager)
                                      ],
                                      debug=True)
  run_wsgi_app(application)

if __name__ == "__main__":
  main()
