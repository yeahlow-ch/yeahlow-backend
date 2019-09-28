from random import random
from firebase_admin import firestore

class Votes:

    DOWNVOTE = 0
    UPVOTE = 1

    def __init__(self, votesCollection):
        self.votes = votesCollection


    def addVote(self, latitude, longitude, vote):
        record = {
            'timestamp' : firestore.SERVER_TIMESTAMP,
            'location' : firestore.GeoPoint(latitude, longitude),
            'vote' : vote
        }

        self.votes.add(record)


    def getHotspots(self):
        hotspots = {}
        for row in self.votes.stream():
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
                'latitude' : location[0],
                'longitude' : location[1],
                'hotness' : hotspots[key]
            })

        return records


    def deleteAll(self):
        for row in self.votes.stream():
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


        
