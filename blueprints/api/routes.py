"""Файл API."""


# -- импорт модулей
from flask import render_template, jsonify
from flask import Blueprint
from flask_restful import reqparse, abort, Api, Resource
from core.models import User, db, Post
import settings

bp = Blueprint('api', __name__)


@bp.route('/', methods=['GET'])
def index():
    return render_template('api.html', title='Api')

@bp.route('/user/<int:user_id>', methods=['GET', 'POST'])
def user(user_id):
    user = User.query.get_or_404(user_id)
    return user.to_dict(only=['id', 'username', 'bio', 'status', 'last_visit', 'registered_at'])

@bp.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return post.to_dict(only=['id', 'category', 'data', 'created_at'])
