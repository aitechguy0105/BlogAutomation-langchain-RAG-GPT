from flask import request, json, Response, Blueprint, jsonify, g
from ..models.UserModel import UserModel, UserSchema
from ..shared.Authentication import Auth

user_api = Blueprint('users', __name__)
user_schema = UserSchema()


@user_api.route('/', methods=['POST'])
def create():
    """
    Create User Function
    """
    req_data = request.get_json()
    try:
        result = user_schema.load(req_data)
        # Continue processing the user data
    except Exception as e:
        e.__str__()
        return custom_response({'error': e.__str__()}, 201)

    if "error" in result:
        return custom_response(result.error, 400)

    # check if user already exist in the db
    user_in_db = UserModel.get_user_by_email(result.get('email'))
    if user_in_db:
        message = {'error': 'User already exist, please supply another email address'}
        return custom_response(message, 200)

    user = UserModel(result)
    user.save()

    ser_data = user_schema.dump(user)

    token = Auth.generate_token(ser_data.get('id'))
    print('token', token)
    return custom_response({'jwt_token': token}, 201)


@user_api.route('/login', methods=['POST'])
def login():
    req_data = request.get_json()

    data = user_schema.load(req_data, partial=True)

    if 'error' in data:
        return custom_response(data.error, 400)

    if not data.get('email') or not data.get('password'):
        return custom_response({'error': 'you need email and password to sign in'}, 200)

    user = UserModel.get_user_by_email(data.get('email'))

    if not user:
        return custom_response({'error': 'no user'}, 200)

    if not user.check_hash(data.get('password')):
        return custom_response({'error': 'password incorrect'}, 200)

    ser_data = user_schema.dump(user)

    token = Auth.generate_token(ser_data.get('id'))

    return custom_response({'jwt_token': token}, 200)
@user_api.route('/', methods=['GET'])
@Auth.auth_required
def get_all():
  users = UserModel.get_all_users()
  ser_users = user_schema.dump(users, many=True)
  return custom_response(ser_users, 200)


@user_api.route('/<int:user_id>', methods=['GET'])
@Auth.auth_required
def get_a_user(user_id):
    """
    Get a single user
    """
    user = UserModel.get_one_user(user_id)
    if not user:
        return custom_response({'error': 'user not found'}, 404)

    ser_user = user_schema.dump(user).data
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['PUT'])
@Auth.auth_required
def update():
    """
    Update me
    """
    req_data = request.get_json()
    data = user_schema.load(req_data, partial=True)
    if 'error' in data:
        return custom_response(data.error, 400)

    user = UserModel.get_one_user(g.user.get('id'))
    user.update(data)
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


@user_api.route('/me', methods=['DELETE'])
@Auth.auth_required
def delete():
    """
    Delete a user
    """
    user = UserModel.get_one_user(g.user.get('id'))
    user.delete()
    return custom_response({'message': 'deleted'}, 204)


@user_api.route('/me', methods=['GET'])
@Auth.auth_required
def get_me():
    """
    Get me
    """
    user = UserModel.get_one_user(g.user.get('id'))
    ser_user = user_schema.dump(user)
    return custom_response(ser_user, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
