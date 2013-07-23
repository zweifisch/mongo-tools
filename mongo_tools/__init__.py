from pymongo import MongoClient
from docopt import docopt
from collections import Counter
from operator import itemgetter
from time import sleep


def print_tabular(head, rows, row_format=None, cell_width=20):
	if row_format is None:
		row_format ="{:>%s}" % cell_width * (len(head))
	print(row_format.format(*head))
	for row in rows:
		 print(row_format.format(*row))

class MongoTask:

	def __init__(self,port,host):
		self.client = MongoClient(port, host)

	def db(self, name=None):
		if name:
			return self.client[name]
		else:
			return self.client[self.client.database_names()[0]]


class Profile(MongoTask):

	def run(self, db, time, duration):
		self.db(db).command({'profile': 1, 'slowms': time})
		sleep(duration)
		self.db(db).command({'profile': 0})
		for row in self.client[db]['system.profile'].find():
			print(row)


class Info(MongoTask):

	def prettyNum(self,num):
		units = list('PTGMK')
		unit = ' '
		while len(units) > 0 and num > 1024:
			num = num / 1024.
			unit = units.pop()
		return "%0.1f %s" % (num, unit)

	def humanNum(self,num):
		units = list('bmk')
		unit = ' '
		while len(units) > 0 and num > 1000:
			num = num / 1000.
			unit = units.pop()
		return "%0.1f %s" % (num, unit)

	def connections(self):

		ips = Counter(x['client'].split(':')[0]
			for x in self.db().current_op(include_all=True)['inprog'] if 'client' in x)
		print_tabular(('ip','counts'), ips.most_common(), cell_width=16)

	def dbs(self,db=None):
		fields = ('ns', 'storageSize', 'size', 'totalIndexSize', 'count')
		mappers = {
				'ns': lambda x:'.'.join(x.split('.')[1:]),
				'storageSize': self.prettyNum,
				'size': self.prettyNum,
				'totalIndexSize': self.prettyNum,
				'count': self.humanNum,
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


def profile():
	"""mongo-profile

Usage:
  mongo-profile <db> <filter> [<duration> --port <port> --host <host>]

Options:
  -h --help            Show this screen.
  --port <port>        Specify mongodb port [default: 27017]
  --host <host>        Specify mongodb host [default: 127.0.0.1]
"""
	args = docopt(profile.__doc__)
	task = Profile(args['--host'], int(args['--port']))
	task.run(args['<db>'], int(args['<filter>']), int(args['<duration>']) if args['<duration>'] else 0)


def info():
	"""mongo-info

Usage:
  mongo-info connections [--port <port> --host <host>]
  mongo-info dbs [--port <port> --host <host>]
  mongo-info db <name> [--port <port> --host <host>]

Options:
  -h --help            Show this screen.
  --port <port>        Specify mongodb port [default: 27017]
  --host <host>        Specify mongodb host [default: 127.0.0.1]
"""
	args = docopt(info.__doc__)
	task = Info(args['--host'], int(args['--port']))
	if (args['connections']):
		task.connections()
	if (args['dbs']):
		task.dbs()
	if (args['db']):
		task.dbs(args['<name>'])
