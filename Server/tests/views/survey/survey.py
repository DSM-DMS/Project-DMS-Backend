import json
import unittest

from tests.views import account_admin, account_student

from app.models.survey import SurveyModel
from server import app


class TestSurvey(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

        account_admin.create_fake_account()
        account_student.create_fake_account()

        self.admin_access_token = account_admin.get_access_token(self.client)
        self.student_access_token = account_student.get_access_token(self.client)

    def tearDown(self):
        account_admin.remove_fake_account()
        account_student.remove_fake_account()
        SurveyModel.objects.delete()

    def testA_addSurvey(self):
        """
        TC about survey addition

        - Preparations
        None

        - Exception Tests
        None

        - Process
        Add survey data

        - Validation
        Check survey data length is 1
        """
        # -- Preparations --
        # -- Preparations --

        # -- Exception Tests --
        # -- Exception Tests --

        # -- Process --
        rv = self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': json.dumps([1, 3])
        })
        self.assertEqual(rv.status_code, 201)
        # -- Process --

        # -- Validation --
        rv = self.client.get('/admin/survey', headers={'Authorization': self.admin_access_token})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(rv.data)
        # -- Validation --

    def testB_deleteSurvey(self):
        """
        TC about survey deletion

        - Preparations
        Add sample survey data
        Take survey ID

        - Exception Tests
        Short survey ID
        Non-existing survey ID

        - Process
        Delete survey data

        - Validation
        Check survey data is empty
        """
        # -- Preparations --
        rv = self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': json.dumps([1, 3])
        })
        self.assertEqual(rv.status_code, 201)
        survey_id = json.loads(rv.data.decode())['id']
        # -- Preparations --

        # -- Exception Tests --
        rv = self.client.delete('/admin/survey', headers={'Authorization': self.admin_access_token}, data={'survey_id': '1234'})
        self.assertEqual(rv.status_code, 204)

        rv = self.client.delete('/admin/survey', headers={'Authorization': self.admin_access_token}, data={'survey_id': '123456789012345678901234'})
        self.assertEqual(rv.status_code, 204)
        # -- Exception Tests --

        # -- Process --
        rv = self.client.delete('/admin/survey', headers={'Authorization': self.admin_access_token}, data={'survey_id': survey_id})
        self.assertEqual(rv.status_code, 200)
        # -- Process --

        # -- Validation --
        rv = self.client.get('/admin/survey', headers={'Authorization': self.admin_access_token})
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(json.loads(rv.data.decode()))
        # -- Validation --

    def testC_addQuestion(self):
        """
        TC about survey question addition

        - Preparations
        Add sample survey data
        Take survey ID
        Check question data is empty

        - Exception Tests
        Short survey ID
        Non-existing survey ID

        - Process
        Add question data

        - Validation
        Check question data length is 1
        """
        # -- Preparations --
        rv = self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': json.dumps([1, 3])
        })
        self.assertEqual(rv.status_code, 201)
        survey_id = json.loads(rv.data.decode())['id']

        rv = self.client.get('/admin/survey/question', headers={'Authorization': self.admin_access_token}, query_string={'survey_id': survey_id})
        self.assertEqual(rv.status_code, 200)
        self.assertFalse(json.loads(rv.data.decode()))
        # -- Preparations --

        # -- Exception Tests --
        rv = self.client.post('/admin/survey/question', headers={'Authorization': self.admin_access_token}, data=json.dumps({'survey_id': '1234'}), content_type='application/json')
        self.assertEqual(rv.status_code, 204)

        rv = self.client.post('/admin/survey/question', headers={'Authorization': self.admin_access_token}, data=json.dumps({'survey_id': '123456789012345678901234'}), content_type='application/json')
        self.assertEqual(rv.status_code, 204)
        # -- Exception Tests --

        # -- Process --
        rv = self.client.post('/admin/survey/question', headers={'Authorization': self.admin_access_token}, data=json.dumps({
            'survey_id': survey_id,
            'questions': [
                {
                    'title': 'test',
                    'is_objective': True,
                    'choice_paper': ['one', 'two', 'three']
                },
                {
                    'title': 'test2',
                    'is_objective': False
                }
            ]
        }), content_type='application/json')
        self.assertEqual(rv.status_code, 201)
        # -- Process --

        # -- Validation --
        rv = self.client.get('/admin/survey/question', headers={'Authorization': self.admin_access_token}, query_string={'survey_id': survey_id})
        self.assertEqual(rv.status_code, 200)
        self.assertTrue(json.loads(rv.data.decode()))
        # -- Validation --

    def testD_answer(self):
        """
        TC about survey answer upload

        - Preparations
        Add sample survey data
        Add sample question data

        - Exception Tests
        Forbidden with admin access token
        Short question ID
        Non-existing question ID

        - Process
        Take questions using student survey APIs
        Add answer data

        - Validation
        Check answer data(API required)
        """
        # -- Preparations --
        rv = self.client.post('/admin/survey', headers={'Authorization': self.admin_access_token}, data={
            'title': 'test',
            'description': 'test',
            'start_date': '2018-01-01',
            'end_date': '2018-12-31',
            'target': json.dumps([1, 3])
        })
        self.assertEqual(rv.status_code, 201)
        survey_id = json.loads(rv.data.decode())['id']

        rv = self.client.post('/admin/survey/question', headers={'Authorization': self.admin_access_token}, data=json.dumps({
            'survey_id': survey_id,
            'questions': [
                {
                    'title': 'test',
                    'is_objective': True,
                    'choice_paper': ['one', 'two', 'three']
                },
                {
                    'title': 'test2',
                    'is_objective': False
                }
            ]
        }), content_type='application/json')
        self.assertEqual(rv.status_code, 201)
        # -- Preparations --

        # -- Exception Tests --
        rv = self.client.post('/survey/question', headers={'Authorization': self.admin_access_token})
        self.assertEqual(rv.status_code, 403)

        rv = self.client.post('/survey/question', headers={'Authorization': self.student_access_token}, data={'question_id': '1234'})
        self.assertEqual(rv.status_code, 204)

        rv = self.client.post('/survey/question', headers={'Authorization': self.student_access_token}, data={'question_id': '123456789012345678901234'})
        self.assertEqual(rv.status_code, 204)
        # -- Exception Tests --

        # -- Process --
        rv = self.client.get('/survey', headers={'Authorization': self.student_access_token})
        self.assertEqual(rv.status_code, 200)
        survey_id = json.loads(rv.data.decode())[0]['id']

        rv = self.client.get('/survey/question', headers={'Authorization': self.student_access_token}, query_string={'survey_id': survey_id})
        self.assertEqual(rv.status_code, 200)
        questions = json.loads(rv.data.decode())

        for question in questions:
            rv = self.client.post('/survey/question', headers={'Authorization': self.student_access_token}, data={
                'question_id': question['id'],
                'answer': 'one'
            })
            self.assertEqual(rv.status_code, 201)
        # -- Process --

        # -- Validation --
        # -- Validation --
