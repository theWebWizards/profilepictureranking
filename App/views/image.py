from flask import Blueprint, render_template, jsonify, request, send_from_directory, redirect
from flask_jwt import jwt_required
from flask_login import login_required, current_user



from App.controllers import (
    createImage, 
    getImage,
    getImage_JSON,
    getAllImages,
    getAllImages_JSON,
    getImagesByUser,
    getImagesByUser_JSON,
    getAverageImageRank,
    getImageRanking,
    getImageRankingJSON,
    deleteImage,
    get_user,
)

image_views = Blueprint('image_views', __name__, template_folder='../templates')




@image_views.route('/addImage',methods=['GET'])
@login_required
def image_page():
    return render_template('addimage.html')

@image_views.route('/newimage', methods=['POST'])
def create_image_action_ui():

    url = request.form.get('url')

    user = current_user
    image = createImage(current_user.id, url)
    return  render_template('profile.html',user=user)


@image_views.route('/addImage', methods=['POST'])
@login_required
def add_image():
    data = request.form
    picture=get_image_by_url(current_user.id,data['url'])
    if picture==None:
        image = create_image(current_user.id, data['url'])
        flash("You just added a new picture to your profile!")
        return redirect(url_for('image_views.image_page'))
    flash('You already uploaded this picture')
    return redirect(url_for('image_views.image_page'))


@image_views.route('/api/image/<int:id>', methods=['GET'])
@jwt_required()
def get_images_action(id):
    image = getImage(id)
    if image:
        return jsonify(getImage_JSON(id)),200
    return jsonify ({"message": "This image was not found"}), 404

@image_views.route('/api/image/user/<int:userId>', methods=['GET'])
@jwt_required()
def get_images_by_user_action(userId):
    user = get_user(userId)
    if not user:
        return jsonify({"message": "This user was not found."}), 404
    images = getImagesbyUser(userId)
    if images: 
        return jsonify(getImagesbyUser_JSON(userId)), 200
    return jsonify({"message": "There are no images by this user."}), 404

@image_views.route('/api/image/<int:imageId>/rank', methods=['GET'])
@jwt_required()
def getAverageImageRank(imageId):
    image= getImage(imageId)
    if image:
        return jsonify(getImageRankingJSON(imageId)), 200
    return jsonify({"message": "This image was not found"}), 404



@image_views.route('/delete/image/<id>')
def delete_image_action(id):
    if getImage(id):
        deleteImage(id)
    return  render_template('profile.html',user=current_user)