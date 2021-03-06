from flask import Blueprint, Response, abort, g, request
from flask_restful import Api
from flasgger import swag_from

from app.docs.v2.admin.post.post import *
from app.models.account import AdminModel
from app.views.v2 import BaseResource, auth_required, json_required
from app.views.v2.admin.post import CATEGORY_MODEL_MAPPING

api = Api(Blueprint(__name__, __name__))
api.prefix = '/admin/post'


@api.resource('/<category>')
class Post(BaseResource):
    @auth_required(AdminModel)
    @json_required({'title': str, 'content': str})
    @swag_from(POST_POST)
    def post(self, category):
        """
        게시글 업로드
        """
        payload = request.json

        if category.upper() not in CATEGORY_MODEL_MAPPING:
            abort(400)

        post = CATEGORY_MODEL_MAPPING[category.upper()](
            author=g.user.name,
            title=payload['title'],
            content=payload['content']
        ).save()

        return {
            'id': str(post.id)
        }, 201


@api.resource('/<category>/<post_id>')
class PostAlteration(BaseResource):
    @auth_required(AdminModel)
    @json_required({'title': str, 'content': str})
    @swag_from(POST_PATCH)
    def patch(self, category, post_id):
        """
        게시글 수정
        """
        payload = request.json

        if category.upper() not in CATEGORY_MODEL_MAPPING:
            abort(400)

        if len(post_id) != 24:
            return Response('', 204)

        post = CATEGORY_MODEL_MAPPING[category.upper()].objects(id=post_id).first()

        if not post:
            return Response('', 204)

        post.update(
            title=payload['title'],
            content=payload['content']
        )

        return Response('', 200)

    @auth_required(AdminModel)
    @swag_from(POST_DELETE)
    def delete(self, category, post_id):
        """
        게시글 삭제
        """
        if category.upper() not in CATEGORY_MODEL_MAPPING:
            abort(400)

        if len(post_id) != 24:
            return Response('', 204)

        post = CATEGORY_MODEL_MAPPING[category.upper()].objects(id=post_id).first()

        if not post:
            return Response('', 204)

        post.delete()

        return Response('', 200)
