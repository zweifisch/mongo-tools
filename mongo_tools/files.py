from .base import MongoTask
from .base import json_encode
from .base import ObjectId
from .base import print_tabular
from .base import pretty_num

class Files(MongoTask):

	def find(self, _id, db):
		f = self.db(db)['fs.files'].find_one({'_id':ObjectId(_id)})
		# print(json_encode(f)), indent=3))
		if f:
			print(f['filename'])
			print(pretty_num(f['length']))
			print(f['uploadDate'])
			print(f['md5'])

	def largest(self, limit, db):
		print_tabular(('size', 'date', 'name'),
			((pretty_num(x['length']), str(x['uploadDate']).split('.')[0], x['filename'].encode('utf8')) for x in
				self.db(db)['fs.files'].find().limit(limit).sort('length', -1)))

	def count(self, db):
		print(self.db(db)['fs.files'].count())
