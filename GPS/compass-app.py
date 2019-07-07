from firebase import Firebase

config = {
    "apiKey": "AIzaSyDZQENVi3p5rZZwC8YaA4tfeB8kFo9bLgA",
    "authDomain": "igp-sensors-readings.firebaseapp.com",
    "databaseURL": "https://igp-sensors-readings.firebaseio.com",
    "projectId": "igp-sensors-readings",
    "storageBucket": "igp-sensors-readings.appspot.com",
    "messagingSenderId": "699634168979",
    "appId": "1:699634168979:web:df476c33c6f57180"
  }

firebase = Firebase(config)

db = firebase.database()
GPS_lat = db.child("GPS").child("lat").get().val()
GPS_long = db.child("GPS").child("long").get().val()
while(True):
	Compass_head = db.child("Compass").child("head").get().val()
	GPS_lat = db.child("GPS").child("lat").get().val()
	GPS_long = db.child("GPS").child("long").get().val()
	print(Compass_head,GPS_lat,GPS_long)
