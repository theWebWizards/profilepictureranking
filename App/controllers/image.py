from App.models import Image
from App.controllers import get_user 
from App.database import db

def createImage(userId, url):
    user = get_user(userId)
    if user:
        image = Image(userId, url)
        db.session.add(image)
        db.session.commit()
        return image
    return None

def getImage(id):
    image = Image.query.get(id)
    return image

def getImage_JSON(id):
    image = Image.query.get(id)
    if image:
        return image.toJSON()
    return[]

def getAllImages():
    images = Image.query.all()
    return images

def getAllImages_JSON():
    images = Image.query.all()
    return[image.toJSON() for image in images]

def getImagesByUser(userId):
    images = Image.query.filter_by(userId = userId).all()
    return images

def getImagesByUser_JSON(userId):
    images = Image.query.filter_by(userId = userId).all()
    return[image.toJSON() for image in images]

def getAverageImageRank(imageId):
    image = getImage(imageId)
    if image:
        return image.getAverageRank()
    return 0

def getImageRanking(imageId):
    image = getImage(imageId)
    if image:
        return image.getAllRankings()
    return[]

def getImageRankingJSON(imageId):
    rank = getImageRanking(imageId)
    return[ranking.toJSON() for ranking in rank]

def deleteImage(id):
    image = getImage(id)
    if image:
        db.session.delete(image)
        db.session.commit()
        return True
    return False