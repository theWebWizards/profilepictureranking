from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required


from App.controllers import (
    createImage, 
    getImage,
    getImage_JSON,
    getAllImages,
    getAllImages_JSON,
    getImagesbyUser,
    getImagesbyUser_JSON,
    getAverageImageRank,
    getImageRanking,
    getImageRankingJSON,
    deleteImage,
    get_user
)

image_views = Blueprint('image_views', __name__, template_folder='../templates')


@image_views.route('/api/images', methods=['POST'])
@jwt_required()
def create_image_action():
    data = request.json
    image = createImage(current_identity.id, data["url"])
    if image:
        image = create_image(data['userId'])
        return jsonify(getImage_JSON((image.getId()))), 201
    return jsonify({"message":"Image unable to post"}), 400

@image_views.route('/api/image/<int:id>', methods=['GET'])
@jwt_required()
def get_images_action(id):
    image = getImage(id)
    if image:
        return jsonify(getImage_JSON(id)),200
    return jsonify ({"message": "This image was not found"}), 404

@image_views.route('/api/image/user/<int: userId>', methods=['GET'])
@jwt_required()
def get_images_by_user_action(userId):
    user = get_user(userId)
    if not user:
        return jsonify({"message": "This user was not found."}), 404
    images = getImagesbyUser(userId)
    if images: 
        return jsonify(getImagesbyUser_JSON(userId)), 200
    return jsonify({"message": "There are no images by this user."}), 404

@image_views.route('/api/image/<int: imageId>/rank', methods=['GET'])
@jwt_required()
def getAverageImageRank(imageId):
    image= getImage(imageId)
    if image:
        return jsonify(getImageRankingJSON(imageId)), 200
    return jsonify({"message": "This image was not found"}), 404

@image_views.route('/api/image/<int: id>', methods=['DELETE'])
@jwt_required()
def delete_image_action():
    curr = deleteImage(id)
    if curr:
        return jsonify({"message":"Image Deleted"}), 200
    return jsonify({"message":"Image Not Found"}), 404