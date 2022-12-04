from App.database import db

class Feed(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    senderId = db.Column(db.Integer, db.ForeignKey("user.id"), nullable = False)
    receiverId = db.Column (db.Integer, db.ForeignKey("user.id"), nullable = False)
    sender = db.relationship("User", foreign_keys=[senderId])
    receiver = db.relationship("User", foreign_keys=[receiverId])
    distributorId = db.Column(db.Integer, db.ForeignKey("distributor.id"), nullable = False)
    seen = db.Column(db.Boolean, default=False)

    def __init__(self, senderId, receiverId, distributorId):
        self.senderId = senderId
        self.receiverId = receiverId
        self.distributorId = distributorId
        self.seen = False

    def getId(self):
        return self.id

    def getDistributorId(self):
        return self.distributorId

    def isSeen(self):
        return self.seen

    def setSeen(self):
        self.seen = True
    
    def to_json(self):
        return{
            "id": self.id,
            "senderId": self.senderId,
            "receiverId": self.receiverId,
            "distributorId": self.distributorId,
            "seen": self.seen,
        }