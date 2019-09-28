from math import sin, cos, sqrt, atan2, radians
from random import *
from datetime import *
from dateutil.parser import parse
from firebase_admin import firestore
from enum import Enum

class DataAccess:

    DOWNVOTE = 0
    UPVOTE = 1

    Type = Enum('Type', 'sport party animal hackathon culture')

    def __init__(self):
        self.votes = []
        self.events = []
        self.addFakeData()


    def addVote(self, latitude, longitude, vote, place):
        record = {
            'timestamp' : datetime.now(),
            'latitude' : latitude,
            'longitude' : longitude,
            'vote' : vote,
            'place': place
        }
        self.votes.append(record)


    def getHotspots(self):
        hotspots = {}
        for row in self.votes:
            if row['vote'] != self.UPVOTE:
                continue

            latitude = '{0:.3f}'.format(row['latitude'])
            longitude = '{0:.3f}'.format(row['longitude'])
            location = latitude + ',' + longitude 
            place = row['place']
            if place in hotspots:
                hot = int(hotspots[place].split(',')[2]) + 1
                hotspots[place] = latitude + ',' + longitude + ',' + str(hot)
            else:
                hotspots[place] = latitude + ',' + longitude + ',' + '1'
        records = []
        for key, val in hotspots.items():
            print(key, val)
            location = val.split(',')
            records.append({
                'latitude' : float(location[0]),
                'longitude' : float(location[1]),
                'hotness' : int(location[2]),
                'place': key
            })

        return records


    def addEvent(self, name, description, event_type, latitude, longitude, start_time, end_time, image_url):
        record = {
            'name' : name,
            'description' : description,
            'type': event_type.name,
            'latitude' : latitude,
            'longitude' : longitude,
            'start_time' : start_time,
            'end_time' : end_time,
            'image_url' : image_url
        }

        self.events.append(record)

    def getEvents(self):
        return self.events


    def getSurpriseEvent(self, longitude, latitude, range):
        candidates = [x for x in self.events
            if self.calculateDistance(
                    longitude,
                    latitude,
                    x['longitude'],
                    x['latitude'])
                <= range]

        return choice(candidates)

    # src: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    def calculateDistance(self, lon1, lat1, lon2, lat2):
        # approximate radius of earth in km
        R = 6373.0

        lat1r = radians(lat1)
        lon1r = radians(lon1)
        lat2r = radians(lat2)
        lon2r = radians(lon2)

        dlon = lon2r - lon1r
        dlat = lat2r - lat1r

        a = sin(dlat / 2)**2 + cos(lat1r) * cos(lat2r) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c

        print(distance)

        return distance


    def addFakeData(self):
        # long, lat, count
        locations = [
            (47.389717, 8.515884, 200, "Foundation Technopark Zurich"), # technopark
            (47.386245, 8.574252, 150, "Zoo Zürich"), # zoo
            (47.379190, 8.539851, 50, "Swiss National Museum"), # national museum
            (47.382547, 8.503395, 150, "Stadion Letzigrund") # letzigrund
        ]

        for loc in locations:
            for i in range(loc[2]):
                self.addVote(
                    loc[0] + random() / 1000, 
                    loc[1] + random() / 1000, 
                    self.UPVOTE,
                    loc[3])

        self.addEvent(
            'HackZurich 2019',
            'Europe\'s biggest Hackathon',
            self.Type.hackathon,
            47.389654,
            8.516268,
            parse('2019-09-27T17:00+02:00'),
            parse('2019-09-29T17:00+02:00'),
            'https://pbs.twimg.com/profile_images/1177302206296600576/QVs8cieJ_400x400.jpg'
        )
        
        self.addEvent(
            'Indiennes. Material for a thousand stories ',
            'In the 17th century indiennes – printed and painted cotton fabrics from India – became a popular commodity in Europe. Western manufacturers, including scores of Swiss companies, started producing their own versions of these precious items and very soon indiennes were everywhere. The exhibition at the National Museum tells the story of the production of these textiles, discusses colonial heritage and travels the trade routes between India, Europe and Switzerland. Very worth seeing are the many sumptuous fabrics, including valuable works on loan from Switzerland and abroad.',
            self.Type.culture,
            47.379095,
            8.540263,
            parse('2019-08-30T00:00+02:00'),
            parse('2020-01-20T00:00+02:00'),
            'https://www.landesmuseum.ch/landesmuseum/ausstellungen/wechselausstellungen/2019/indiennes/image-thumb__4044__header_image/indiennes-header-landingpage~-~767w@2x.jpeg'
        )

        self.addEvent(
            'GC - FC Chiasso',
            'Challenge League Match',
            self.Type.sport,
            47.382641,
            8.540263,
            parse('2019-09-28T17:30+02:00'),
            parse('2019-09-28T19:30+02:00'),
            'https://upload.wikimedia.org/wikipedia/commons/4/43/Letzigrund_Zuerich.jpg'
        )

        self.addEvent(
            'Geneva',
            'Something far away to test',
            self.Type.party,
            46.176820,
            6.040197,
            parse('2019-09-28T17:30+02:00'),
            parse('2019-09-28T19:30+02:00'),
            'https://upload.wikimedia.org/wikipedia/commons/thumb/9/9d/Wappen_Genf_matt.svg/1280px-Wappen_Genf_matt.svg.png'
        )