from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    create_ranking,
    get_rankings_by_ranker,
    get_rankings_by_image,
    get_ranking,
    get_ranking_json,
    get_all_rankings,
    get_all_rankings_json,
    get_rankings_by_ranker,
    get_rankings_by_ranker_json,
    get_rankings_by_image,
    get_rankings_by_image_json,
    update_ranking,
    delete_ranking,
    get_user,
    getImage
)

ranking_views = Blueprint('ranking_views', __name__, template_folder='../templates')

@ranking_views.route('/api/rankings', methods=['POST'])
@jwt_required()
def create_ranking_action():
    data = request.json
    if get_user(data['rankerId']) and get_image(data['imageId']):
        ranking = create_ranking(data["rankerId"], data["imageId"], data["rank"])
        return jsonify(get_all_rankings_json(ranking.getId())), 201
    elif not get_user(data["rankerId"]):
        return jsonify ({"message": "This ranker does not exist"}), 404
    elif not getImage(data["imageId"]):
        return jsonify ({"message": "This image does not exist."}), 404
    else: 
        return jsonify ({"message" : "Error"}), 500

@ranking_views.route('/api/ranking/<int:id>', methods=['GET'])
@jwt_required()
def get_ranking_action(id):
    ranking = get_ranking(id)
    if ranking:
        return jsonify(get_ranking_json(id)), 200
    else: 
        return jsonify({"message": "Does not exist."}), 404

@ranking_views.route('/api/rankings/ranker/<int:rankerId>', methods=['GET'])
@jwt_required()
def get_rankings_by_ranker_action(rankerId):
    user = get_user(rankerId)
    if not user:
        return jsonify({"message": "This ranker does not exist"})
    rankings = get_rankings_by_ranker(rankerId)
    if rankings:
        return jsonify(get_rankings_by_ranker_json(rankerId)), 200
    return jsonify({"message":"Rankings Not Found"}), 404

@ranking_views.route('/api/rankings/image/<int:imageId>', methods=['GET'])
@jwt_required()
def get_rankings_by_image_action(imageId):
    image = getImage(imageId)
    if not image:
        return jsonify({"message": "This image does not exist"}), 404
    rankings = get_rankings_by_image(imageId)
    if rankings:
       return jsonify(get_rankings_by_image_json(imageId)), 200
    else:
        return jsonify({"message":"These rankings do not exist"}), 404

@ranking_views.route('/api/rankings/<int:id>', methods=['PUT'])
@jwt_required()
def update_ction(id):
    data = request.json
    status = update_ranking(id, data["rank"])
    if status:
       return jsonify(get_rankings_by_image(id)), 200
    else:
        return jsonify({"message": "This ranking does not exist."})


@ranking_views.route('/api/rankings/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_ranking_action(id):
    curr = delete_ranking(id)
    if curr:
        return jsonify({"message": "Ranking was deleted"}), 200
    else:
        return jsonify({"message": "This ranking does not exist"}), 404
     

