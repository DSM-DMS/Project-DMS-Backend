import json

from flask import Response
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restful import Resource, request
from flasgger import swag_from

from app.docs.admin.point.point import *
from app.models.account import AdminModel, StudentModel
from app.models.point import PointRuleModel, PointHistoryModel


class PointManaging(Resource):
    @swag_from(POINT_MANAGING_GET)
    @jwt_required
    def get(self):
        """
        특정 학생의 상벌점 내역 조회
        """
        admin = AdminModel.objects(id=get_jwt_identity()).first()
        if not admin:
            return Response('', 403)

        id = request.form['id']
        student = StudentModel.objects(id=id).first()
        if not student:
            return Response('', 204)

        response = [{
            'time': str(history.time)[:-7],
            'reason': history.reason.name,
            'point': history.point
        } for history in student.point_histories]

        return Response(json.dumps(response, ensure_ascii=False), 200, content_type='application/json; charset=utf8')

    @swag_from(POINT_MANAGING_POST)
    @jwt_required
    def post(self):
        """
        특정 학생에 대한 상벌점 부여
        """
        admin = AdminModel.objects(id=get_jwt_identity()).first()
        if not admin:
            return Response('', 403)

        id = request.form['id']
        student = StudentModel.objects(id=id).first()
        if not student:
            return Response('', 204)

        rule_id = request.form['rule_id']
        rule = PointRuleModel.objects(id=rule_id).first()
        if not rule:
            return Response('', 205)

        point = int(request.form['point'])

        student.point_histories.append(PointHistoryModel(
            reason=rule,
            point=point
        ))
        # Append history

        if point < 0:
            student.bad_point += abs(point)
        else:
            student.good_point += point

        student.save()

        return Response('', 201)
