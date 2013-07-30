from .base import MongoTask
from .base import print_tabular
from .base import pretty_num
from .base import human_num
from collections import Counter
from operator import itemgetter


class Info(MongoTask):

	def connections(self):

		ips = Counter(x['client'].split(':')[0]
			for x in self.db().current_op(include_all=True)['inprog'] if 'client' in x)
		print_tabular(('ip','counts'), ips.most_common(), cell_width=16)

	def dbs(self,db=None):
		fields = ('ns', 'storageSize', 'size', 'totalIndexSize', 'count')
		mappers = {
				'ns': lambda x:'.'.join(x.split('.')[1:]),
				'storageSize': pretty_num,
				'size': pretty_num,
				'totalIndexSize': pretty_num,
				'count': human_num,
		}
		getfields = itemgetter(*fields)
		db_names = [db] if db else self.client.database_names()
		for db_name in db_names:
			print(db_name)
			db = self.db(db_name)
			coll_infos = (db.command({"collStats":coll_name}) for coll_name in db.collection_names())
			rows = map(list,map(getfields, coll_infos))
			for row in rows:
				for  idx,field in enumerate(fields):
					if field in mappers:
						row[idx] = mappers[field](row[idx])
			print_tabular(fields, rows)

