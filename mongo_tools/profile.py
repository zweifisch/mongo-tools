from time import sleep
import datetime
from .base import MongoTask
from .base import json_encode

class Profile(MongoTask):

	def start(self, db, time, duration):
		self.db(db).command({'profile': 1, 'slowms': time})
		if duration:
			sleep(duration)
			self.stop(db)
			self.report(db, duration)

	def stop(self, db):
		self.db(db).command({'profile': 0})

	def report(self, db, seconds):
		time = datetime.datetime.utcnow() - datetime.timedelta(seconds=seconds)
		for row in self.client[db]['system.profile'].find({'ts':{'$gt':time}}).sort('millis', -1):
			row['ts'] = str(row['ts'])
			print(json_encode(row, indent=3))
