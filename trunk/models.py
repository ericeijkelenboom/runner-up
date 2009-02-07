from google.appengine.ext import db

class FoodItem(db.Model):
  name = db.StringProperty(multiline=False)
  kcals = db.IntegerProperty()

class Route(db.Model):
    name = db.StringProperty()

class Vertex(db.Model):
    lat = db.FloatProperty()
    lng = db.FloatProperty()
    route = db.ReferenceProperty(Route)