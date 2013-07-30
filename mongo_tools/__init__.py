from docopt import docopt
from .info import Info
from .profile import Profile
from .files import Files


def profile():
	"""mongo-profile

Usage:
  mongo-profile start <db> <filter> [<duration> --port <port> --host <host>]
  mongo-profile stop <db> [--port <port> --host <host>]
  mongo-profile report <db> <duration> [--port <port> --host <host>]

Options:
  -h --help            Show this screen.
  --port <port>        Specify mongodb port [default: 27017]
  --host <host>        Specify mongodb host [default: 127.0.0.1]
"""
	args = docopt(profile.__doc__)
	task = Profile(args['--host'], int(args['--port']))
	if (args['start']):
		task.start(args['<db>'], int(args['<filter>']), int(args['<duration>']) if args['<duration>'] else 0)
	elif (args['stop']):
		task.stop(args['<db>'])
	elif (args['report']):
		task.report(args['<db>'], int(args['<duration>']))


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


def files():
	"""
Usage:
  mongo-files find <id> <db> [--port <port> --host <host>]
  mongo-files largest <limit> <db> [--port <port> --host <host>]
  mongo-files count <db> [--port <port> --host <host>]

Options:
  -h --help            Show this screen.
  --port <port>        Specify mongodb port [default: 27017]
  --host <host>        Specify mongodb host [default: 127.0.0.1]
"""
	args = docopt(files.__doc__)
	task = Files(args['--host'], int(args['--port']))
	if(args['find']):
		task.find(args['<id>'], args['<db>'])
	elif(args['largest']):
		task.largest(int(args['<limit>']), args['<db>'])
	elif(args['count']):
		task.count(args['<db>'])
