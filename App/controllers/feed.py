from App.models import Feed
from App.database import db

def create_feed(send_id, receive_id, distributor_id):
    feed = Feed(send_id, receive_id, distributor_id)
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

def get_sender_feeds(send_id):
    feeds = Feed.query.filter_by(send_id = send_id).all()
    return feeds

def get_sender_feeds_json(send_id):
    feeds = Feed.query.filter_by(send_id = send_id).all()
    return [feed.to_json() for feed in feeds]

def get_receiver_feeds(receive_id):
    feeds = Feed.query.filter_by(receive_id = receive_id).all()
    return feeds

def get_receiver_feeds_json(receive_id):
    feeds = Feed.query.filter_by(receive_id = receive_id).all()
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