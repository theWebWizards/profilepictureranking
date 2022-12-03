from App.database import db
from datetime import date

#Ratings are created by users when they rate other users' profiles
#Timestamps solve the 'limited number of ratings a day' problem
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raterId =  db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    ratedId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    rater = db.relationship("User", foreign_keys=[raterId])
    rated = db.relationship("User", foreign_keys =[ratedId])
    rating = db.Column(db.Integer, nullable=False)
    
    def __init__(self, raterId, ratedId, rating):
        self.raterId = raterId
        self.ratedId = ratedId
        self.rating = rating
    
    def toJSON(self):
        return{
            'id': self.id,
            'raterId': self.raterId,
            'ratedId': self.ratedId,
            'rating': self.rating, 
        }

