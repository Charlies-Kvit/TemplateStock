from data import db_session
from flask_restful import abort, Resource, reqparse
from .posts import Post
from flask import abort

parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('user_id', type=int)


def abort_if_post_not_found(post_id):
    db_sess = db_session.create_session()
    posts = db_sess.query(Post).get(post_id)
    db_sess.close()
    if not posts:
        abort(404, f'Post {post_id} not found')


class PostsResource(Resource):
    def get(self, post_id):
        abort_if_post_not_found(post_id)
        db_sess = db_session.create_session()
        posts = db_sess.query(Post).get(post_id)
        db_sess.close()
        return {'post': posts.to_dict(only=('id', 'title', 'content', 'created_date', 'is_private', 'user_id'))}

    def put(self, post_id):
        abort_if_post_not_found(post_id)
        args = parser.parse_args()
        db_sess = db_session.create_session()
        post = db_sess.query(Post).get(post_id)
        post.title = args['title']
        post.content = args['content']
        post.is_private = args['is_private']
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}

    def delete(self, post_id):
        abort_if_post_not_found(post_id)
        db_sess = db_session.create_session()
        post = db_sess.query(Post).get(post_id)
        db_sess.delete(post)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}


class PostsListResource(Resource):
    def get(self):
        db_sess = db_session.create_session()
        posts = db_sess.query(Post).all()
        db_sess.close()
        return {'posts': [post.to_dict(only=('id', 'title', 'content', 'created_date', 'is_private', 'user_id'))
                          for post in posts]}

    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        post = Post(
            title=args['title'],
            content=args['content'],
            is_private=args['is_private'],
            user_id=args['user_id']
        )
        db_sess.add(post)
        db_sess.commit()
        db_sess.close()
        return {'success': 'OK'}
