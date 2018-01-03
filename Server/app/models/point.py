from datetime import datetime

from app.models import *


class PointRuleModel(Document):
    """
    Point rules
    """
    meta = {
        'collection': 'point_rule'
    }

    name = StringField(
        required=True
    )


class PointHistoryModel(EmbeddedDocument):
    """
    Good/bad point in dormitory of each students
    """
    meta = {
        'collection': 'point_history'
    }

    time = DateTimeField(
        required=True,
        default=datetime.now()
    )

    reason = ReferenceField(
        document_type=PointRuleModel,
        required=True
    )
    point = IntField(
        required=True
    )
