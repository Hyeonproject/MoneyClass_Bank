from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator

import uuid

class TimeStampedModel(models.Model):
    created = fields.DatetimeField(auto_now_add=True)
    modified = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True

class Account(TimeStampedModel):
    '''
    계좌
    '''
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    email = fields.CharField(max_length=100, unique=True)
    balances = fields.BigIntField(default=0)

    def __str__(self):
        return self.id

class Transaction(models.Model):
    '''
    거래 내역
    '''
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    transaction_date = fields.DatetimeField(auto_now_add=True)
    account_id = fields.ForeignKeyField('models.Account', related_name='transaction')
    amount = fields.IntField()
    receiver = fields.CharField(max_length=100)
    note = fields.TextField(null=True)

    def __str__(self):
        return '{} :: {}'.format(self.id, self.amount)

class AdminLog(models.Model):
    '''
    관리자 사용 이력
    '''
    id = fields.UUIDField(pk=True, default=uuid.uuid4())
    use_datetime = fields.DatetimeField(auto_now_add=True)
    role = fields.CharField(max_length=20)
    usage_details = fields.CharField(max_length=30)
    note = fields.TextField(null=True)

Account_Pydantic = pydantic_model_creator(Account, name='Account')
AccountIn_Pydantic = pydantic_model_creator(Account, name='AccountIn', exclude_readonly=True)
Transcation_Pydantic = pydantic_model_creator(Transaction, name='Transcation')
TranscationIn_Pydantic = pydantic_model_creator(Transaction, name='TranscationIn', exclude_readonly=True)
AdminLog_Pydantic = pydantic_model_creator(AdminLog, name='AdminLog')
AdminLogIn_Pydantic = pydantic_model_creator(AdminLog, name='AdminLogIn', exclude_readonly=True)