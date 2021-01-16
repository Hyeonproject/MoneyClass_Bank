from tortoise import fields, models
from tortoise.contrib.pydantic import pydantic_model_creator


class CreatedModel(models.Model):
    created = fields.DatetimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Customers(CreatedModel):
    """
    고객 테이블
    """
    id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=50, unique=True)
    role = fields.CharField(max_length=25)

    def __str__(self):
        return self.email


class Accounts(CreatedModel):
    """
    계좌 테이블
    """
    id = fields.UUIDField(pk=True)
    balance = fields.IntField(default=0)
    modified = fields.DatetimeField(auto_now=True)
    customers = fields.OneToOneField(
        'models.Customers', related_name='CustomerToAccount'
    )


class Transcations(models.Model):
    """
    거래 내역 테이블
    """
    id = fields.UUIDField(pk=True)
    date = fields.DatetimeField(auto_now_add=True)
    amount = fields.IntField()
    account = fields.ForeignKeyField('models.Accounts', related_name='account')
    customer = fields.ForeignKeyField('models.Customers', related_name='customer_trans')
    trans_type = fields.ForeignKeyField('models.TranscationType', related_name='trans_type')


class TranscationType(models.Model):
    """
    거래 타입을 추가할 수 있습니다. 이체 등등 적용 예정
    """
    id = fields.IntField(pk=True)
    trans_type_name = fields.CharField(max_length=30, unique=True)


# Pydantic
Customers_Pydantic = pydantic_model_creator(Customers, name='Customers')
Accounts_Pydantic = pydantic_model_creator(Accounts, name='Accounts')
TranscationType_Pydantic = pydantic_model_creator(TranscationType, name='TranscationType')
Transcations_Pydantic = pydantic_model_creator(Transcations, name='Transcations')