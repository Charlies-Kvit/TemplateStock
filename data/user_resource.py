from data import db_session
from flask_restful import abort, Resource, reqparse
from .users import User
from flask import abort, jsonify


parser = reqparse.RequestParser()
parser.add_argument('login', required=True)
parser.add_argument('email', required=True)
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('password', required=True)


def abort_if_news_not_found(users_id):
    session = db_session.create_session()
    users = session.query(User).get(users_id)
    if not users:
        abort(404, f"User {users_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_news_not_found(user_id)
        db_sess = db_session.create_session()
        user = db_sess.query(User).get(user_id)
        return jsonify(
            {'user': user.to_dict(only=('id', 'login', 'surname', 'name', 'email', 'hashed_password', 'date_change',
                                        'date_create'))})


class UsersListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        users = db_sess.query(User).all()
        return jsonify({
            'users':
                    [item.to_dict(only=('id', 'login', 'surname', 'name', 'email', 'hashed_password', 'date_change',
                                        'date_create'))
                     for item in users
                     ]
        })

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        user = User(
            login=args['login'],
            email=args['email'],
            surname=args['surname'],
            name=args['name'],
        )
        user.set_password(args['password'])
        db_sess.add(user)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}
