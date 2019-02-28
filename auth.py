from models.base import db, app, bcrypt
from models.user import UserCred, UserInfo, TokenList
from flask import request, make_response, jsonify


@app.route('/register', methods=['POST'])
def user_register():
    data = request.form
    user = UserCred(data['login'], data['password'])

    if not UserCred.query.filter_by(login=data['login']).first():
        db.session.add(user)
        db.session.commit()
        return 'Registration success', 200
    else:
        return 'User exists', 200

@app.route('/login', methods=['POST'])
def user_login():
    data = request.form
    try:
        user = UserCred.query.filter_by(login=data['login']).first()
        if bcrypt.check_password_hash(user.pw_hash, data['password']):
            auth_token = user.create_auth_token()
            if auth_token:
                token = TokenList(auth_token, user.user_id)
                db.session.add(token)
                db.session.commit()
                responseObj = {
                    'auth_token': auth_token
                }
                return make_response(jsonify(responseObj)), 200
    except Exception as e:
        responseObj = {
            'status': 'fail'
        }
        return make_response(jsonify(responseObj)), 500


@app.route('/logout', methods=['POST'])
def user_logout():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        result = TokenList.query.filter_by(token=auth_token).first()
        if result:
            try:
                db.session.delete(result)
                db.session.commit()
                responseObj = {
                    'message': 'Logged out'
                }
                return make_response(jsonify(responseObj)), 200
            except Exception as e:
                responseObj = {
                    'status': 'fail',
                    'message': e
                }
                return make_response(jsonify(responseObj)), 200
        else:
            responseObj = {
                'message': 'Fail'
            }
            return make_response(jsonify(responseObj)), 401
    else:
        responseObj = {
            'status': 'fail',
            'message': 'Invalid token'
        }
        return make_response(jsonify(responseObj)), 403

@app.route('/user_info', methods=['PUT', 'GET'])
def user_info():
    auth_header = request.headers.get('Authorization')
    if auth_header:
        auth_token = auth_header.split(" ")[1]
    else:
        auth_token = ''
    if auth_token:
        id = TokenList.query.filter_by(token=auth_token).first()
    else:
        return 'Access is forbidden', 403

    if request.method == 'PUT':
        if id:
            data = request.form
            info = UserInfo.query.filter_by(user_id=id.user_id).first()
            if not info:
                info_add = UserInfo(id.user_id)
                db.session.add(info_add)
                db.session.commit()
                info_add.update_fields(data)
            else:
                info.update_fields(data)
            db.session.commit()
            responseObj = {
                'message': 'User info updated'
            }
            return make_response(jsonify(responseObj)), 200
        else:
            return 'Access is forbidden', 403

    if request.method == 'GET':
        if id:
            info = UserInfo.query.filter_by(user_id=id.user_id).first()
            if info:
                responseObj = {
                    'name': info.name,
                    'surname': info.surname,
                    'age': info.age
                }
            else:
                responseObj = {
                    'name': '',
                    'surname': '',
                    'age': ''
                }
            return make_response(jsonify(responseObj)), 200
        else:
            return 'Access is forbidden', 403

