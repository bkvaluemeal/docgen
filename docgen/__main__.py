from docgen import types
import argparse
import docgen
import os
import sys

def main():
	'''
	The main method and entry point of the application
	'''

	parser = argparse.ArgumentParser(
		description = 'docgen v%s' % docgen.__version__,
		epilog = 'Copyright (c) 2017, Justin Willis',
		prog = 'docgen',
		formatter_class = argparse.RawTextHelpFormatter
	)
	parser.add_argument(
		'-v', '--version',
		action = 'version',
		version = 'docgen v%s' % docgen.__version__
	)
	parser.add_argument(
		'package',
		help = 'the name of the package in the current directory',
		default = os.path.relpath('.', '..'),
		nargs = '?'
	)
	args = parser.parse_args()
	sys.path.append(os.getcwd())

	print('Generating documentation for package %s:\n' % args.package)

	for mod in types.Package(args.package).save():
		print(mod)

	print('\n%s' % os.path.join(os.getcwd(), 'docs'))

if __name__ == '__main__':
	main()
