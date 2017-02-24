'''
Utility functions for documentation generation
'''

from math import ceil, floor
import re

PRIMS = {
	'tuple': 'Tuple',
	'int': 'Integer',
	'str': 'String',
	'dict': 'Dictionary',
	'chr': 'Character',
	'char': 'Character',
	'unichr': 'Unicode Character',
	'ord': 'Ordinal',
	'hex': 'Hexadecimal',
	'oct': 'Octal'
}

class _Table(object):
	'''
	A table

	Args:
		title (str): The name of the table
	'''

	def __init__(self, title):
		self.title = title.title()
		self.rows = []
		self.cols = []

	def add_col(self, name):
		'''
		Adds a column to the table

		Args:
			name (str): The name of the column
		'''

		self.cols.append(name)

	def add_row(self, **columns):
		'''
		Adds a row to the table

		Args:
			**columns (str): The text to fill the columns
		'''

		if 'type' in columns:
			if columns['type'].lower() in PRIMS:
				columns['type'] = PRIMS[columns['type'].lower()]

		self.rows.append(columns)

	def __str__(self):
		result = '**%s:**\n\n|' % self.title
		header = ''
		col_widths = {}

		for col in self.cols:
			w = 0

			for row in self.rows:
				l = len(row[col]) + 2

				if l > w:
					w = l

			col_widths[col] = max(w, len(col) + 2)
			p = max(1, (w - len(col)) / 2)

			header += '%s%s%s|' % (
				' ' * floor(p),
				col.title(),
				' ' * ceil(p)
			)

		result += header + '\n' + '|'

		for col in self.cols:
			result += '-' * col_widths[col] + '|'

		result += '\n'

		for row in self.rows:
			result += '|'

			for col in self.cols:
				result += ' %s%s |' % (
					row[col],
					' ' * (col_widths[col] - len(row[col]) - 2)
				)

			result += '\n'

		return result

def gen_tables(doc):
	'''
	Processes a docstring and replaces lists with tables

	Args:
		doc (str): The docstring to process
	'''

	result = ''

	lines = doc.split('\n')
	i = 0
	while i < len(lines):
		line = lines[i].strip()

		if line == 'Args:':
			args = _Table('args')
			args.add_col('name')
			args.add_col('type')
			args.add_col('description')

			i += 1
			line = lines[i].strip()
			while len(line) > 0 and i < len(lines):
				cols = re.findall('^(.*) \(([^\W]+)\): (.*)', line)[0]
				args.add_row(
					name = cols[0],
					type = cols[1].title(),
					description = cols[2]
				)
				i += 1

				try:
					line = lines[i].strip()
				except:
					pass

			result += str(args) + '\n'
		elif line == 'Raises:':
			raises = _Table('raises')
			raises.add_col('type')
			raises.add_col('description')

			i += 1
			line = lines[i].strip()
			while len(line) > 0 and i < len(lines):
				cols = re.findall('^(.*): (.*)', line)[0]
				raises.add_row(
					type = cols[0],
					description = cols[1]
				)
				i += 1

				try:
					line = lines[i].strip()
				except:
					pass

			result += str(raises) + '\n'
		elif line == 'Returns:':
			returns = _Table('returns')
			returns.add_col('type')
			returns.add_col('description')

			i += 1
			line = lines[i].strip()
			while len(line) > 0 and i < len(lines):
				ret_type = 'Object'
				for key, value in PRIMS.items():
					if key in line or value in line:
						ret_type = value
						break

				returns.add_row(
					type = ret_type.title(),
					description = line
				)
				i += 1

				try:
					line = lines[i].strip()
				except:
					pass

			result += str(returns) + '\n'
		else:
			result += line + '\n'

		i += 1

	return result
