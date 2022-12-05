from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_rating,
    get_ratings_by_rater,
    get_ratings_by_rater_json,
    get_ratings_by_ratee,
    get_ratings_by_ratee_json,
    get_rating,
    get_rating_json,
    get_all_ratings,
    get_all_ratings_json,
    update_rating,
    delete_rating,
    get_user
)

rating_views = Blueprint('rating_views', __name__, template_folder='../templates')


@rating_views.route('/api/ratings', methods=['POST'])
@jwt_required()
def create_rating_action():
    data = request.json
    if get_user(data['raterId']) and get_user(data['rateeId']):
        rating = create_rating(data['raterId'], data['rateeId'], data['rating'])
        return jsonify(get_rating_json(rating.getId())), 201
    elif not get_user(data["raterId"]):
        return jsonify({"message": "This rater does not exist"}), 404
    elif not get_user(data["rateeId"]):
        return jsonify({"message": "This ratee does exist."}),404
    else:
        return jsonify({"message": "An error occurred."}), 500

@rating_views.route('/api/ratings/<int:id>', methods=['GET'])
@jwt_required()
def get_rating_action(id):
    rating = get_rating(id)
    if rating:
        return jsonify(get_rating_json(id)), 200
    else:
        return jsonify({"message": "This rating does not exist"}), 404

@rating_views.route('/api/ratings/rater/<int:raterId>', methods=['GET'])
@jwt_required()
def get_rating_by_rater_action(raterId):
    rating = get_ratings_by_rater(raterId)
    if rating:
        return jsonify(get_ratings_by_rater_json(raterId)), 200
    return jsonify({"message":"Rating not found"}), 404 

@rating_views.route('/api/ratings/rater/<int:ratee_id>', methods=['GET'])
@jwt_required()
def get_rating_by_ratee_action(rateeId):
    rating = get_ratings_by_ratee(rateeId)
    if rating:
        return jsonify(get_ratings_by_rateee(rateeId)), 200
    return jsonify({"message":"Rating not found"}), 404 

@rating_views.route('/api/ratings/<int:id>', methods=['PUT'])
@jwt_required()
def update_rating_action(id):
    data = request.json
    curr = update_rating(id, data['rating'])
    if curr:
        return jsonify(get_rating_json(id)),200
    else:
        return jsonify({"message":"Rating not found"}), 404 

@rating_views.route('/api/ratings/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_rating_action(id):
    curr = delete_rating(id)
    if curr:
        return jsonify({"message": "This rating was deleted"}), 200
    else:
        return jsonify({"message":"Rating does not exist"}), 404 

