from App.database import db
from datetime import datetime

class Distributor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numOfProfiles = db.Column(db.Integer, nullable = False)
    feed = db.relationship("Feed", backref="distributor", lazy=True, cascade="all, delete-orphan")
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, numOfProfiles):
        self.numOfProfiles = numOfProfiles
    
    def getId(self):
        return self.id
    
    def getNumofProfiles(self):
        return self.num_of_profiles
    
    def getTimeStamp(self):
        return self.timestamp
    
    def getReceivers(self):
        receivers = []
        for feed in self.feed:
            receivers.append(feed.receiverId)
        return receivers
    
    def get_senders(self):
        senders = []
        for feed in self.feed:
            senders.append(feed.senderId)
        return senders

    def to_json(self):
        return {
            "id" :self.id,
            "numOfProfiles": self.numOfProfiles,
            "timestamp": self.timestamp
        }