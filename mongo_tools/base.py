import json
import datetime
from pymongo import MongoClient
from pymongo.son_manipulator import ObjectId


class JSONEncoder(json.JSONEncoder):
	def default(self, o):
		if isinstance(o, ObjectId):
			return str(o)
		elif isinstance(o, datetime.datetime):
			return str(0)
		return json.JSONEncoder.default(self, o)


def json_encode(obj, **kargs):
	return JSONEncoder(**kargs).encode(obj)


def print_tabular(head, rows, row_format=None, cell_width=20):
	if row_format is None:
		row_format ="{:>%s} " % cell_width * (len(head))
	print(row_format.format(*head))
	for row in rows:
		 print(row_format.format(*row))


def pretty_num(num):
	units = list('PTGMK')
	unit = ' '
	while len(units) > 0 and num > 1024:
		num = num / 1024.
		unit = units.pop()
	return "%0.1f %s" % (num, unit)


def human_num(num):
	units = list('bmk')
	unit = ' '
	while len(units) > 0 and num > 1000:
		num = num / 1000.
		unit = units.pop()
	return "%0.1f %s" % (num, unit)


class MongoTask:

	def __init__(self,port,host):
		self.client = MongoClient(port, host)

	def db(self, name=None):
		if name:
			return self.client[name]
		else:
			return self.client[self.client.database_names()[0]]

