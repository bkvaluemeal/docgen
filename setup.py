from setuptools import setup, find_packages

def format(input, start = 0):
	result = ''
	indent = False
	count = 0

	with open(input, 'r') as file:
		for line in file:
			if count > start:
				if line[:1] == '\t' and not indent:
					indent = True
					result += '::\n\n'

				if line[:1].isalnum() and indent:
					indent = False

				result += line.replace('> ', '\t').replace('>', '\t')
			count += 1

	return result

blurb = ('Docgen is a Python module that generates markdown documentation for'
 	' Python code that adheres to Google\'s style guide.\n'
)

setup(
	name = 'docgen',
	version = '0.1.0',
	author = 'Justin Willis',
	author_email = 'sirJustin.Willis@gmail.com',
	packages = find_packages(),
	include_package_data = True,
	zip_safe = False,
	url = 'https://bitbucket.org/bkvaluemeal/docgen',
	license = 'ISC License',
	description = 'A markdown documentation generator for Python',
	long_description = blurb + format('README.md', 3),
	entry_points = {
		'console_scripts': [
			'docgen = docgen.__main__:main'
		]
	},
	classifiers = [
		'Development Status :: 3 - Alpha',
		'Environment :: Console',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: ISC License (ISCL)',
		'Operating System :: OS Independent',
		'Programming Language :: Python :: 3',
		'Topic :: Documentation'
	],
	keywords = 'markdown documentation generator',
	install_requires = [
	]
)
