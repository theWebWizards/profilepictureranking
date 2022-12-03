from App.models import Feed
from App.database import db

def create_feed(senderId, receiverId, distributorId):
    feed = Feed(senderId, receiverId, distributorId)
    db.session.add(feed)
    db.session.commit()
    return feed

def get_feed(id):
    feed = Feed.query.get(id)
    return feed

def get_feed_jsom(id):
    feed = Feed.query.get(id)
    return feed.to_json()

def get_all_feed():
    feed = Feed.query.all()
    return feed

def get_all_feed_json():
    feed = Feed.query.all()
    return [feed.to_json() for feed in feed]

def get_sender_feeds(senderId):
    feeds = Feed.query.filter_by(senderId = senderId).all()
    return feeds

def get_sender_feeds_json(senderId):
    feeds = Feed.query.filter_by(senderId = senderId).all()
    return [feed.to_json() for feed in feeds]

def get_receiver_feeds(receiverId):
    feeds = Feed.query.filter_by(receiverId = receiverId).all()
    return feeds

def get_receiver_feeds_json(receiverId):
    feeds = Feed.query.filter_by(receiverId = receiverId).all()
    return [feed.to_json() for feed in feeds]

def feed_view(id):
    feed = Feed.query.get(id)
    if feed:
        feed.set_seen()
        db.session.commit()
        return feed
    return None

def feed_delete(id):
    feed = Feed.query.get(id)
    if feed:
        db.session.delete()
        return db.session.commit()
    return None