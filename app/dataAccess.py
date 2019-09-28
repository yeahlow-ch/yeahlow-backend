from random import random
from dateutil.parser import *
from datetime import *
import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("./firebase_key.json")
firebase_admin.initialize_app(cred)

class DataAccess:

    DOWNVOTE = 0
    UPVOTE = 1

    def __init__(self):
        self.votes = firestore.client().collection('votes')
        self.events = firestore.client().collection('events')


    def addVote(self, latitude, longitude, vote):
        record = {
            'timestamp' : firestore.SERVER_TIMESTAMP,
            'location' : firestore.GeoPoint(latitude, longitude),
            'vote' : vote
        }

        self.votes.add(record)


    def getHotspots(self):
        hotspots = {}
        for row in self.votes.where(u'vote', u'==', self.UPVOTE).stream():
            doc = row.to_dict()
            latitude = '{0:.3f}'.format(doc['location'].latitude)
            longitude = '{0:.3f}'.format(doc['location'].longitude)
            location = latitude + ',' + longitude

            if location in hotspots:
                hotspots[location] += 1
            else:
                hotspots[location] = 1

        records = []
        for key in hotspots:
            location = key.split(',')
            records.append({
                'latitude' : float(location[0]),
                'longitude' : float(location[1]),
                'hotness' : hotspots[key]
            })

        return records


    def addEvent(self, name, description, latitude, longitude, start_time, end_time, image_url):
        record = {
            'name' : name,
            'description' : description,
            'location' : firestore.GeoPoint(latitude, longitude),
            'start_time' : start_time,
            'end_time' : end_time,
            'image_url' : image_url
        }

        self.events.add(record)


    def getEvents(self):
        records = []
        for row in self.events.stream():
            doc = row.to_dict()
            records.append({
                'name' : doc['name'],
                'description' : doc['description'],
                'latitude' : doc['location'].latitude,
                'longitude' : doc['location'].longitude,
                'start_time' : doc['start_time'],
                'end_time' : doc['end_time'],
                'image_url' : doc['image_url']
            })

        return records


    def deleteAll(self):
        for row in self.votes.stream():
            row.reference.delete()

        for row in self.events.stream():
            row.reference.delete()

    
    def addFakeData(self):
        # long, lat, count
        locations = [
            (47.389717, 8.515884, 200), # technopark
            (47.386245, 8.574252, 150), # zoo
            (47.379190, 8.539851, 50), # national museum
            (47.382547, 8.503395, 150) # letzigrund
        ]

        for loc in locations:
            for i in range(loc[2]):
                self.addVote(
                    loc[0] + random() / 1000, 
                    loc[1] + random() / 1000, 
                    self.UPVOTE)

        self.addEvent(
            'HackZurich 2019',
            'Europe\'s biggest Hackathon',
            47.389654,
            8.516268,
            parser.parse('2019-09-27 17:00 +02:00'),
            parser.parse('2019-09-29 17:00 +02:00'),
            'https://pbs.twimg.com/profile_images/1177302206296600576/QVs8cieJ_400x400.jpg'
        )
        
        self.addEvent(
            'Indiennes. Material for a thousand stories ',
            'In the 17th century indiennes – printed and painted cotton fabrics from India – became a popular commodity in Europe. Western manufacturers, including scores of Swiss companies, started producing their own versions of these precious items and very soon indiennes were everywhere. The exhibition at the National Museum tells the story of the production of these textiles, discusses colonial heritage and travels the trade routes between India, Europe and Switzerland. Very worth seeing are the many sumptuous fabrics, including valuable works on loan from Switzerland and abroad.',
            47.379095,
            8.540263,
            parser.parse('2019-08-30 00:00 +02:00'),
            parser.parse('2020-01-20 00:00 +02:00'),
            'https://www.landesmuseum.ch/landesmuseum/ausstellungen/wechselausstellungen/2019/indiennes/image-thumb__4044__header_image/indiennes-header-landingpage~-~767w@2x.jpeg'
        )

        self.addEvent(
            'GC - FC Chiasso',
            'Challenge League Match',
            47.382641,
            8.540263,
            parser.parse('2019-09-28 17:30 +02:00'),
            parser.parse('2019-09-28 19:30 +02:00'),
            'https://upload.wikimedia.org/wikipedia/commons/4/43/Letzigrund_Zuerich.jpg'
        )