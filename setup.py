from setuptools import setup

setup(
	name='mongo-tools',
	url='https://github.com/zweifisch/mongo-tools',
	version='0.0.1',
	description='cli utility for mongodb',
	author='Feng Zhou',
	author_email='zf.pascal@gmail.com',
	packages=['mongo_tools'],
	install_requires=['docopt', 'blessings', 'pymongo'],
	entry_points={
		'console_scripts': ['mongo-info=mongo_tools:info',
			'mongo-profile=mongo_tools:profile'],
	},
)
