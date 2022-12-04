from App.models import Rating, User
from App.database import db

def create_rating(raterId, rateeId, rating):
    rater = get_user(raterId)
    ratee = get_user(rateeId)
    if rater and ratee:
         newRating = Rating(raterId=raterId, rateeId=rateeId, rating=rating)
         db.session.add(newRating)
         db.session.commit()
         return newRating
    return None

def get_ratings_by_rater(raterId):
    ratings = Rating.query.filter_by(raterId=raterId).all()
    return ratings

def get_ratings_by_rater_json(raterId):
    ratings = Rating.query.filter_by(raterId=raterId).all()
    return [rating.toJSON() for rating in ratings]

def get_ratings_by_ratee(rateeId):
    ratings = Rating.query.filter_by(rateeId=rateeId).all()
    return ratings

def get_ratings_by_ratee_json(rateeId):
    ratings = Rating.query.filter_by(rateeId=rateeId).all()
    return [rating.toJSON() for rating in ratings]

def get_rating(id):
    rating = Rating.query.get(id)
    return rating

def get_rating_json(id):
    rating = Rating.query.get(id)
    return rating.to_json()

def get_all_ratings():
    ratings = Rating.query.all()
    return ratings

def get_all_ratings_json():
    ratings = Rating.query.all()
    return [rating.toJSON() for rating in ratings]

def update_rating(id, rating):
    rating = Rating.query.get(id)
    if rating:
        rating.set_rating(new_rating)
        db.session.commit()
        return rating
    return None

def delete_rating(id):
     rating = Rating.query.get(id)
     if rating:
         db.session.delete(rating)
         db.session.commit()
         return True
     return False
