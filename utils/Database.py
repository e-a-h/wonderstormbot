from peewee import MySQLDatabase, Model, PrimaryKeyField, BigIntegerField, CharField, ForeignKeyField, AutoField

from utils import Configuration

connection = MySQLDatabase(Configuration.get_var("DATABASE_NAME"),
                           user=Configuration.get_var("DATABASE_USER"),
                           password=Configuration.get_var("DATABASE_PASS"),
                           host=Configuration.get_var("DATABASE_HOST"),
                           port=Configuration.get_var("DATABASE_PORT"), use_unicode=True, charset="utf8mb4")


class BugReport(Model):
    id = AutoField()
    reporter = BigIntegerField()
    message_id = BigIntegerField(unique=True, null=True)
    attachment_message_id = BigIntegerField(unique=True, null=True)
    platform = CharField(10)
    platform_version = CharField(20)
    branch = CharField(10)
    app_version = CharField(20)
    title = CharField(200, collation="utf8mb4_general_ci")
    steps = CharField(1024, collation="utf8mb4_general_ci")
    expected = CharField(100, collation="utf8mb4_general_ci")
    actual = CharField(100, collation="utf8mb4_general_ci")
    additional = CharField(500, collation="utf8mb4_general_ci")

    class Meta:
        database = connection


class Attachements(Model):
    id = AutoField()
    url = CharField(collation="utf8mb4_general_ci")
    report = ForeignKeyField(BugReport, backref="attachments")

    class Meta:
        database = connection


class Repros(Model):
    id = AutoField()
    user = BigIntegerField()
    report = ForeignKeyField(BugReport, backref="repros")

    class Meta:
        database = connection


def init():
    global connection
    connection.connect()
    connection.create_tables([BugReport, Attachements, Repros])
    connection.close()