from peewee import *
from pyenv import ENV

db_name = ENV.FM_DB_NAME
db_user = ENV.FM_DB_USER
db_password = ENV.FM_DB_PWD
db_host = ENV.FM_DB_HOST
db_schema = ENV.FM_DB_SCHEMA
db = PostgresqlDatabase(database=db_name, user=db_user, password=db_password, host=db_host, port=5439)


class BaseModel(Model):
    dmjl_ins_sysdate = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])
    dmjl_upd_sysdate = DateTimeField(constraints=[SQL('DEFAULT CURRENT_TIMESTAMP')])

    class Meta:
        database = db
        schema = db_schema


class File(BaseModel):
    dmjl_data_source = CharField()
    dmjl_filename = CharField(unique=True)
    dmjl_download_url = CharField()
    dmjl_storage_url = CharField()

    class Meta:
        table_name = 'daemon_jrnl'
        # Redshift doesn't support serial data type, i.e. no primary key
        primary_key = False


def create_tables():
    with db:
        db.create_tables([File])
