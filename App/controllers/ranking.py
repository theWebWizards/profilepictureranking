from App.models import Ranking, User, Image
from App.database import db
from App.controllers import get_user, getImage

def create_ranking(rankerId, imageId, rank):
    image = getImage(imageId)
    ranker = get_user(rankerId)
    if ranker and image:
        newRanking = Ranking(rankerId=rankerId, imageId=imageId, rank=rank)
        db.session.add(newRanking)
        db.session.commit()
        return newRanking
    return None

def get_rankings_by_ranker(rankerId, imageId):
    if User.query.get(rankerId) and Image.query.get(imageId):
        rankings = Ranking.query.filter_by(rankerId= rankerId, imageId= imageId).first()
    return rankings



def get_rankings_by_image(imageId):
     rankings = Ranking.query.filter_by(imageId=imageId).all()
     return rankings

def get_ranking(id):
    ranking = Ranking.query.get(id)
    return ranking

def get_ranking_json():
    ranking = Ranking.query.get(id)
    return ranking.to_json()

def get_all_rankings():
    return Ranking.query.all()

def get_all_rankings_json():
    rankings = Ranking.query.all()
    return [ranking.to_json() for ranking in rankings]

def get_rankings_by_ranker(rankerId):
    rankings = Ranking.query.filter_by(rankerId=rankerId).all()
    return rankings

def get_rankings_by_ranker_json(rankerId):
    rankings = Ranking.query.filter_by(creatorId=creatorId).all()
    return [ranking.to_json() for ranking in rankings]

def get_rankings_by_image(imageId):
    rankings = Ranking.query.filter_by(imageId=imageId).all()
    return rankings

def get_rankings_by_image_json(imageId):
    rankings = Ranking.query.filter_by(imageId=imageId).all()
    return [ranking.to_json() for ranking in rankings]

def update_ranking(id, rank):
    ranking = Ranking.query.get(id)
    if ranking:
        ranking.rank = rank
        db.session.commit()
        return ranking
    return None

def delete_ranking(id):
    ranking = Ranking.query.get(id)
    if ranking:
        db.session.delete(ranking)
        db.session.commit()
        return True
    return False