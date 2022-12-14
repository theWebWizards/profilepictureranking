from App.database import db

#Rankings are created by users when they rate other users' pictures
class Ranking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    rankerId =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    imageId =  db.Column(db.Integer, db.ForeignKey('image.id'), nullable=False)
    rank = db.Column(db.Integer, nullable=False)
    
    
    def __init__(self, rankerId, imageId, rank):
        self.rankerId = rankerId
        self.imageId = imageId
        self.rank = rank

    def getId(self):
        return self.id

    def getRankerId(self):
        return self.rankerId

    def getImageId(self):
        return self.imageId

    def getRank(self):
        return self.rank
    
    def toJSON(self):
        return{
            'id': self.id,
            'rankerId': self.rankerId,
            'imageId': self.imageId,
            'rank': self.rank,
        }