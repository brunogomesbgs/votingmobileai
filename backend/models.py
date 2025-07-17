from tortoise.models import Model
from tortoise import fields
from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# Tortoise ORM Models
class Feature(Model):
    id = fields.IntField(pk=True)
    title = fields.CharField(max_length=255)
    description = fields.TextField()
    created_by = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)
    vote_count = fields.IntField(default=0)

    class Meta:
        table = "features"


class Vote(Model):
    id = fields.IntField(pk=True)
    feature = fields.ForeignKeyField('models.Feature', related_name='votes')
    voter_id = fields.CharField(max_length=100)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "votes"
        unique_together = ("feature", "voter_id")


# Pydantic Models for validation
class FeatureCreate(BaseModel):
    title: str
    description: str
    created_by: str


class FeatureResponse(BaseModel):
    id: int
    title: str
    description: str
    created_by: str
    created_at: datetime
    vote_count: int


class VoteCreate(BaseModel):
    feature_id: int
    voter_id: str


class VoteResponse(BaseModel):
    id: int
    feature_id: int
    voter_id: str
    created_at: datetime


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None