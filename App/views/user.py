from flask import Blueprint, render_template, jsonify, request, send_from_directory
from flask_jwt import jwt_required, current_identity


from App.controllers import (
    create_user, 
    getUserbyUsername,
    get_user,
    get_user_json,
    get_all_users,
    get_all_users_json,
    update_user,
    delete_user,
    getImagesByUser_JSON,
    get_average_rate_by_ratee,
    get_ratings_by_ratee_json,
    distribute_all
)

user_views = Blueprint('user_views', __name__, template_folder='../templates')


@user_views.route('/users', methods=['GET'])
@jwt_required()
def get_current_user():
    return jsonify(
        {
            "id" : current_identity.id,
            "username": current_identity.username,
        }
    )

@user_views.route('/api/users', methods=['POST'])
@jwt_required()
def create_user_action():
    data = request.json
    user = getUserbyUsername(data['username'])
    if user:
        return jsonify({"message":"Username Already Taken"}), 400
    user = create_user(data["username"], data["password"])
    if user:
        distribute_all()
        return jsonify({"message": "User Creates"}), 201
    return jsonify({"message":"User not Created"}), 400

@user_views.route('/api/users', methods=['GET'])
@jwt_required()
def get_all_users_action():
    users = get_all_users_json()
    if users:
        return jsonify(users), 200
    return jsonify({"message": "There were no users found."}), 404

@user_views.route('/api/users/<int:id>', methods=['GET'])
@jwt_required()
def get_user_action():
    user = get_user(id)
    if user:
        return jsonify(get_user_json(id)),200
    return jsonify({"message":"User Not Found"}), 404

@user_views.route('/api/users/<int:id>/details', methods=['GET'])
@jwt_required()
def get_user_details_action():
    user = get_user(id)
    if user:
        details = {
            "id": user.getId(),
            "username": user.getUsername(),
            "images": getImagesByUser_JSON(user.getId()),
            "average_rate": get_average_rate_by_ratee(user.getId()),
            "ratings_completed": get_ratings_by_ratee_json(user.getId())
        }
        return jsonify(details),200
    return jsonify({"message":"User Not Found"}), 404

@user_views.route('/api/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user_action():
     data = request.json
     curr = update_user(id, data['username'])
     if curr:
        return jsonify(get_user_json(id)),200
     else:
        return jsonify({"message":"User not found"}), 404 

@user_views.route('/api/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user_action(id):
    user = get_user(id)
    if user:
        delete_user(id)
        return jsonify({"message":"User Deleted"}) , 200
    return jsonify({"message":"User Not Found"}) , 404

#login routes
@user_views.route('/login',methods=['GET'])
def getLoginPage():
    return render_template('login.html')

@user_views.route('/login',methods=['POST'])
def loginAction():
    data=request.form
    permittedUser=authenticate(data['username'], data['password'])
    if permittedUser==None:
        flash("Wrong Credentials, Please try again")
        return redirect(url_for('user_views.getLoginPage'))
    login_user(permittedUser,remember=True)
    flash('You were successfully logged in!')
    return redirect(url_for('distributer_views.view_profiles_again'))