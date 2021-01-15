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
    customer = fields.OneToOneField('models.Customers', related_name='customer_account')


class Transcations(CreatedModel):
    """
    거래 내역 테이블
    """
    id = fields.UUIDField(pk=True)
    date = fields.DatetimeField(auto_now_add=True)
    amount = fields.IntField()
    account = fields.ForeignKeyField('models.Accounts', related_name='account')
    customer = fields.ForeignKeyField('models.Customers', related_name='customer_trans')
    trans_type = fields.ForeignKeyField('models.TranscationType', related_name='trans_type')

    def __str__(self):
        return '{} -> {}'.format(self.account_id, self.customer_id)


class TranscationType(models.Model):
    """
    거래 타입을 추가할 수 있습니다. 이체 등등 적용 예정
    """
    id = fields.IntField(pk=True)
    trans_type_name = fields.CharField(max_length=30, unique=True)

class AdminFunctions(models.Model):
    """
    관리자 기능 테이블
    """
    id = fields.IntField(pk=True)
    func_name = fields.CharField(max_length=50)


class AdminLogs(models.Model):
    """
    관리자 권한 사용 로그 테이블
    """
    id = fields.UUIDField(pk=True)
    admin_funcs = fields.ForeignKeyField('models.AdminFunctions', related_name='func')
    customer = fields.ForeignKeyField('models.Customers', related_name='customer_log')


# Pydantic
Customers_Pydantic = pydantic_model_creator(Customers, name='Customers')
Accounts_Pydantic = pydantic_model_creator(Accounts, name='Accounts')
TranscationType_Pydantic = pydantic_model_creator(TranscationType, name='TranscationType')