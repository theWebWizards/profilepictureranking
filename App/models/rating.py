from App.database import db
from datetime import date

#Ratings are created by users when they rate other users' profiles
#Timestamps solve the 'limited number of ratings a day' problem
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raterId =  db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ratedId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rater = db.relationship("User", foreign_keys=[raterId])
    ratee = db.relationship("User", foreign_keys =[ratedId])
    rating = db.Column(db.Integer, nullable=False)
    
    def __init__(self, raterId, ratedId, rating):
        self.raterId = raterId
        self.rateeId = ratedId
        self.rating = rating

    def getId(self):
        return self.id

    def getRating(self):
        return self.rating

    def getRaterId(self):
        return self.raterId

    def getRateeId(self):
        return self.rateeId

    def setRating(self, newRating):
        self.rating = newRating
    
    def toJSON(self):
        return{
            'id': self.id,
            'raterId': self.raterId,
            'rateeId': self.ratedId,
            'rating': self.rating, 
        }

