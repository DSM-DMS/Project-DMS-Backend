from app_v1.models import *

from app_v1.models.apply import ExtensionApplyModel, GoingoutApplyModel, StayApplyModel
from app_v1.models.point import PointHistoryModel


class SignupWaitingModel(Document):
    """
    Data before the student's signup
    """
    meta = {
        'collection': 'signup_waiting',
    }

    uuid = StringField(
        primary_key=True
    )
    name = StringField(
        required=True
    )
    number = IntField(
        required=True,
        min_value=1101,
        max_value=3421
    )


class AccountBase(Document):
    """
    DMS account_admin Base Document
    """
    meta = {
        'collection': 'account_base',
        'abstract': True,
        'allow_inheritance': True
    }

    signup_time = DateTimeField()

    id = StringField(
        primary_key=True
    )
    pw = StringField(
        required=True
    )
    name = StringField(
        required=True
    )


class StudentModel(AccountBase):
    """
    Student account model
    """
    number = IntField(
        required=True,
        min_value=1101,
        max_value=3421
    )

    extension_apply_11 = EmbeddedDocumentField(
        document_type=ExtensionApplyModel
    )
    extension_apply_12 = EmbeddedDocumentField(
        document_type=ExtensionApplyModel
    )
    goingout_apply = EmbeddedDocumentField(
        document_type=GoingoutApplyModel
    )
    stay_apply = EmbeddedDocumentField(
        document_type=StayApplyModel
    )

    good_point = IntField(
        default=0
    )

    bad_point = IntField(
        default=0
    )

    point_histories = EmbeddedDocumentListField(
        document_type=PointHistoryModel
    )

    penalty_training_status = BooleanField(
        required=True,
        default=False
    )
    penalty_level = IntField(
        required=True,
        default=0
    )


class AdminModel(AccountBase):
    """
    Admin account model
    """


class SystemModel(AccountBase):
    """
    System account model
    """


class RefreshTokenModel(Document):
    """
    Manages JWT refresh token
    """
    meta = {
        'collection': 'refresh_token'
    }

    token = UUIDField(
        primary_key=True
    )
    token_owner = ReferenceField(
        document_type=AccountBase,
        required=True
    )
    pw_snapshot = StringField(
        required=True
    )