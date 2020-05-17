from peewee import *
import datetime

db = SqliteDatabase("pa.db", pragmas={'foreign_keys': 1})
db.connect()


class BaseModel(Model):
	class Meta:
		database = db


class Community(BaseModel):
	name = CharField()
	color = CharField()


class Member(BaseModel):
	name = CharField()
	community = ForeignKeyField(Community, on_delete='RESTRICT')


class Meeting(BaseModel):
	date = DateField()


class Vote(BaseModel):
	number = IntegerField(unique=True)
	meeting = ForeignKeyField(Meeting, on_delete='RESTRICT')


class VoteMember(BaseModel):
	member = ForeignKeyField(Member)
	vote = ForeignKeyField(Vote, on_delete='RESTRICT')


if __name__ == '__main__':
	db.create_tables([Community, Member, Meeting, Vote, VoteMember])
