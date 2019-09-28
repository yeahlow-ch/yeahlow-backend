from math import sin, cos, sqrt, atan2, radians
from random import *
from datetime import *
from dateutil.parser import parse
from enum import Enum
import csv


class DataAccess:

    DOWNVOTE = 0
    UPVOTE = 1

    Type = Enum('Type', 'sport party animal hackathon culture food')

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

    def deleteAll(self):
        self.votes = []
        self.events = []

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
            location = val.split(',')
            hot = int(location[2])
            if 250 <= hot:
                hot_color = '#700000'
            elif 150 <= hot <= 249:
                hot_color = '#f20000'
            elif 50 <= hot <= 149:
                hot_color = '#ff6600'
            else:
                hot_color = '#ffe20a'
            records.append({
                'latitude' : float(location[0]),
                'longitude' : float(location[1]),
                'hotness' : hot,
                'hotness_color': hot_color,
                'place': key
            })

        return records


    def addEvent(self, id, name, description, event_type, latitude, longitude, start_time, end_time):
        record = {
            'id': id,
            'name' : name,
            'description' : description,
            'type': event_type.name,
            'latitude' : latitude,
            'longitude' : longitude,
            'start_time' : start_time,
            'end_time' : end_time
        }

        self.events.append(record)

    def getEvents(self):
        return self.events


    def getSurpriseEvent(self, longitude, latitude, range):
        candidates = [x for x in self.events
            if (range * 0.9) <= self.calculateDistance(
                    longitude,
                    latitude,
                    x['longitude'],
                    x['latitude'])
                <= range * 1.1]
        if not candidates:
            event_distances = []
            for event in self.events:
                distance = self.calculateDistance(longitude, latitude, event['longitude'], event['latitude'])
                if distance > range:
                    continue 

                event_distances.append({'distance': distance, 'event':event})
            return sorted(event_distances, key = lambda x: x['distance'], reverse=True)[0]['event']
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
        locations = []
        with open('./data/locations.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                locations.append((
                    float(row[0]),
                    float(row[1]),
                    int(row[2]),
                    row[3]))

        for loc in locations:
            for i in range(loc[2]):
                self.addVote(
                    loc[0] + random() / 1000, 
                    loc[1] + random() / 1000, 
                    self.UPVOTE,
                    loc[3])

        events = []
        with open('./data/events.csv', 'r') as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            for row in reader:
                events.append(row)

        for i in range(len(events)):
            self.addEvent(
                i+1,
                events[i][0],
                events[i][1],
                self.Type[events[i][2]],
                float(events[i][3]),
                float(events[i][4]),
                parse(events[i][5]),
                parse(events[i][6])
            )