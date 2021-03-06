import copy
from datetime import datetime
from unittest import TestCase as TC

from flask import Response
import pymongo

from app import create_app
from config.test import TestConfig
from app.models.account import AdminModel, StudentModel
from app.models.token import AccessTokenModelV2, RefreshTokenModelV2


class TCBase(TC):
    def __init__(self, *args, **kwargs):
        self.app = create_app(TestConfig)

        mongo_setting = copy.copy(self.app.config['MONGODB_SETTINGS'])
        self.db_name = mongo_setting.pop('db')
        self.mongo_client = pymongo.MongoClient(**mongo_setting)

        self.client = self.app.test_client()

        self.today = datetime.now().strftime('%Y-%m-%d')
        self.now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        self.token_regex = '([\w\-\_]+\.){2}[\w\-\_]+'

        super(TCBase, self).__init__(*args, **kwargs)

    def _create_fake_account(self):
        self.admin = AdminModel(
            id=self.admin_id,
            pw=self.encrypted_pw,
            name=self.admin_name
        ).save()

        self.student = StudentModel(
            id=self.student_id,
            pw=self.encrypted_pw,
            name=self.student_name,
            number=self.student_number
        ).save()

    def _get_tokens(self):
        with self.app.app_context():
            self.admin_access_token = 'JWT {}'.format(AccessTokenModelV2.create_access_token(self.admin, 'TEST'))
            self.admin_refresh_token = 'JWT {}'.format(RefreshTokenModelV2.create_refresh_token(self.admin, 'TEST'))

            self.student_access_token = 'JWT {}'.format(AccessTokenModelV2.create_access_token(self.student, 'TEST'))
            self.student_refresh_token = 'JWT {}'.format(RefreshTokenModelV2.create_refresh_token(self.student, 'TEST'))

    def setUp(self):
        self.admin_id = self.admin_name = 'admin'
        self.student_id = self.student_name = 'student'
        self.student_number = 3118
        self.pw = 'pw'
        self.encrypted_pw = self.encrypt_password(self.pw)

        self._create_fake_account()
        self._get_tokens()

    def tearDown(self):
        self.mongo_client.drop_database(self.db_name)

    def request(self, method, target_url_rule, token=None, *args, **kwargs):
        """
        Helper for common request

        Args:
            method (func): Request method
            target_url_rule (str): URL rule for request
            token (str) : JWT or OAuth's access token with prefix(Bearer, JWT, ...)

        Returns:
            Response
        """
        return method(
            target_url_rule if target_url_rule.startswith('/v2') else '/v2' + target_url_rule,
            headers={'Authorization': token or self.admin_access_token},
            *args,
            **kwargs
        )

    def encrypt_password(self, password):
        with self.app.app_context():
            from app.views.v2 import BaseResource

            return BaseResource.encrypt_password(password)

    def validate_auth_response(self, resp):
        data = resp.json
        self.assertIsInstance(data, dict)

        self.assertIn('accessToken', data)
        self.assertIn('refreshToken', data)

        access_token = data['accessToken']
        refresh_token = data['refreshToken']

        self.assertIsInstance(access_token, str)
        self.assertIsInstance(refresh_token, str)

        self.assertRegex(access_token, self.token_regex)
        self.assertRegex(refresh_token, self.token_regex)

        import jwt

        access_token_identity = jwt.decode(access_token, self.app.secret_key, 'HS256')['identity']
        refresh_token_identity = jwt.decode(refresh_token, self.app.secret_key, 'HS256')['identity']

        self.assertEqual(str(AccessTokenModelV2.objects[AccessTokenModelV2.objects.count() - 1].identity), access_token_identity)
        self.assertEqual(str(RefreshTokenModelV2.objects[RefreshTokenModelV2.objects.count() - 1].identity), refresh_token_identity)
