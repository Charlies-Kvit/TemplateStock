from data import db_session
from flask_restful import abort, Resource, reqparse
from .users import User
from flask import abort, jsonify
import datetime


parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('email', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('password')


def abort_if_user_not_found(user_id):
    session = db_session.create_session()
    users = session.query(User).get(user_id)
    session.close()
    if not users:
        abort(404, f"User {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.close()
        return jsonify(
            {'user': user.to_dict(only=('id', 'login', 'surname', 'name', 'email', 'date_change',
                                        'date_create'))})

    def put(self, user_id):
        abort_if_user_not_found(user_id)
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        user.name = args['name']
        user.surname = args['surname']
        user.email = args['email']
        user.login = args['login']
        user.date_change = datetime.datetime.now()
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}

    def delete(self, user_id):
        abort_if_user_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        db_sess.delete(user)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        db_sess.close()
        return jsonify({
            'users':
                    [user.to_dict(only=('id', 'login', 'surname', 'name', 'email', 'date_change',
                                        'date_create'))
                     for user in users
                     ]
        })

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(
            login=args['login'],
            email=args['email'],
            surname=args['surname'],
            name=args['name']
        )
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}
