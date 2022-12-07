from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect,  url_for

from flask_jwt import jwt_required, current_identity
from flask import Flask,flash
from flask_login import LoginManager, current_user, login_required

from App.models import feed, distributor, user

from datetime import datetime

from App.controllers import *

feed_views = Blueprint('feed_views', __name__, template_folder='../templates')

@feed_views.route('/api/feeds', methods=['GET'])
def create_feed_action():

    if(current_user.feed == []):
        users=User.query.all()
        numprofiles=len(users)
        dist = create_dist(numprofiles)
        feed = create_feed( current_user.id , dist.id )
        #test to see if multiple feeds works
        #feed = create_feed( current_user.id , dist.id )

    dist = get_last_distribution()

    h=dist.timeStamp.hour
    m=dist.timeStamp.minute+2
    interval = datetime.time(hour=h, minute=m)

    expiretime = datetime.datetime.combine(dist.timeStamp, interval)

    #flash("timestamp: ")
    #flash(dist.timeStamp)
    flash("Feed will expire: ")
    flash(expiretime)
    #flash("        now: ")
    #flash(datetime.datetime.now())
    
    if(datetime.datetime.now() > expiretime  ):     
        users=User.query.all()
        numprofiles=len(users)
        dist = create_dist(numprofiles)
        feed = create_feed( current_user.id , dist.id )
        

    feeds = get_feed_by_receiverID(current_user.id)

    for feed in feeds:
        dist = get_dist_by_id(feed.distID)
        h=dist.timeStamp.hour
        m=dist.timeStamp.minute+2
        if m>59:
            m= m%59
            h=h+1
        interval = datetime.time(hour=h, minute=m)
        expiretime = datetime.datetime.combine(dist.timeStamp, interval)

        if (datetime.datetime.now() < expiretime):
            user=get_user(feed.senderID)
            #flash("user: ")
            #flash(user)
            return render_template('feed.html', user=user, feeds= feeds)
    user=get_user(feed.senderID)
    return render_template('feed.html', user=user, feeds= feeds)
    #users = [get_user(feed.senderID) for feed in feeds]
    
            







@feed_views.route('/api/feed', methods=['GET'])
def view_all_feed():
    
    feeds = get_feed_by_receiverID(current_user.id)
    users = [get_user(feed.senderID) for feed in feeds]

    return render_template('feed.html', users=users, feeds= feeds)




