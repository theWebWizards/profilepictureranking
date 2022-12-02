from App.database import db

#Images uploaded by users
class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userId =  db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    url = db.Column(db.String(120), nullable=False)
    rankings = db.relationship('Ranking', backref='image', lazy=True, cascade="all, delete-orphan")

    def __init__(self, userId, url):
        self.userId = userId
        self.url = url
    
    def getId(self):
        return self.id
    
    def getUserId(self):
        return self.userId

    def setUserId (self, userId):
        self.userId = userId
    
    def getURL(self):
        return self.url
    
    def setURL(self, url):
        self.url = url
    
    def getAllRankings(self):
        return self.rankings
    
    def getAverageRank(self):
        rankings = self.rankings
        if len(rankings) == 0:
            return 0
        total = 0 
        for ranking in rankings:
            total += ranking.rank
        return total/ len(rankings)
    
    def toJSON(self):
        return{
            'id': self.id,
            'userId': self.userId,
            'rank': self.getAverageRank(),
            'num_of_rankings': len(self.rankings),
            "url": self.url,
        }
