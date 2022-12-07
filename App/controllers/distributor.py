from App.database import db
from App.models import Distributor
from App.controllers import (
    create_feed,
    get_sender_feeds,
    get_receiver_feeds,
)

from App.controllers.user import get_all_users
from datetime import timedelta, datetime

def create_distributor():

    num_users = len(get_all_users())

    if num_users > 2:
        distributor = Distributor(num_users)
        db.session.add(distributor)
        db.session.commit()
        return distributor

    return None

def get_distributor(id):
    distributor = Distributor.query.get(id)
    return distributor


def get_distributor_json(id):
    distributor = Distributor.query.get(id)
    return distributor.to_json()


def get_all_distributors():
    distributors = Distributor.query.all()
    return distributors


def get_all_distributors_json():
    distributors = Distributor.query.all()
    return [distributor.to_json() for distributor in distributors]


def get_distributor_feeds(id):
    distributor = Distributor.query.get(id)

    if distributor:
        return distributor.feed

    return None


def delete_distributor(id):
    distributor = Distributor.query.get(id)

    if distributor:
        db.session.delete(distributor)
        db.session.commit()
        return True

    return False


def distribute():
    senders = []
    receivers = []
    distributor = create_distributor()

    if distributor:

        for receiverId in range (1, distributor.numOfProfiles+1):

            rec_feeds = get_receiver_feeds(receiverId)
            daily_rec_feeds = len(                  #num of feeds received by receiver
                [
                    feed
                    for feed in rec_feeds
                    if feed.distributor.timestamp >= (datetime.now() - timedelta(days=1))

                ]
            )

            if daily_rec_feeds < distributor.numOfProfiles:

                for senderId in range (1, distributor.numOfProfiles+1):
                    
                    daily_sent_feeds = len(         #num of feeds sent by sender
                        [
                            feed 
                            for feed in get_sender_feeds(senderId)
                            if feed.distributor.timestamp >= (datetime.now() - timedelta(days=1))
                        ]
                    )

            if daily_sent_feeds < distributor.numOfProfiles:

                received = any(
                    feed.senderId == senderId for feed in rec_feeds
                )   

                if (                                #if feed from sender not received then feed created
                    (receiverId != senderId)
                    and not received
                    and (senderId not in senders)
                ):

                    create_feed(senderId, receiverId, distributor.id)
                    senders.append(senderId)
                    receivers.append(receiverId)
                    break

            if len(receivers) < distributor.numOfProfiles:  #if receiver received less than num of profiles per day, more can be received
                                                            
                for receiverId in range(1, distributor.numOfProfiles+1):

                    if receiverId not in receivers:

                        daily_rec_feeds = len(
                            [
                                feed 
                                for feed in get_receiver_feeds(receiverId)
                                if feed.distributor.timestamp >= (datetime.now() - timedelta(days=1))
                            ]
                        )

                     # if sender has sent less than the number of profiles per day then more can be sent
                     # if the sender and receiver not equal and the sender did not send a feed then create feed
                    if (   

                        daily_sent_feeds < distributor.numOfProfiles
                        and senderId != receiverId
                        and senderId not in senders
                    ):

                     create_feed(senderId, receiverId, distributor.id)
                     senders.append(senderId)
                     receivers.append(receiverId)
                     break

            if len(senders) == 0 or len(receivers) == 0:

                return False

            return True

def distribute_all():
    current = distribute()
    count = 1
    while current:
        current = distribute()
        count = count+1
    return count

def get_dist_table():
    distributors = get_all_distributors()
    table = {0: {"Feed ID", "Receiver", "Sender", "Distributor", "Seen"}}

    for distributor in distributors:

        for feed in distributor.feed:
            table[feed.id] = {
                feed.id,
                feed.receiverId,
                feed.senderId,
                feed.distributorId,
                feed.seen,
            }

        return table

def get_completed_dist_table():
    distributors = get_all_distributors()
    table = {0: {"Feed ID", "Receiver", "Sender", "Distributor", "Seen"}}

    for distributor in distributors:
        for feed in distributor.feed:

            if feed.seen:
                table[feed.id] = {
                    feed.id,
                    feed.receiverId,
                    feed.senderId,
                    feed.distributorId,
                    feed.seen,
                }
    return table

def get_incomplete_dist_table():
    distributors = get_all_distributors()
    table = {0: {"Feed ID", "Receiver", "Sender", "Distributor", "Seen"}}

    for distributor in distributors:
        for feed in distributor.feed:

            if not feed.seen:
                table[feed.id] = {
                    feed.id,
                    feed.receiverId,
                    feed.senderId,
                    feed.distributorId,
                    feed.seen,
                }
    return table












