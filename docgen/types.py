'''
Object types for documentation generation

This module defines various containers for organizing the parts of a Python
package.
'''

from docgen import util
import inspect
import os
import textwrap

class Function(object):
	'''
	A function

	Args:
		func (function): The function to wrap
		is_top (bool): Is this function in the top level
	'''

	def __init__(self, func, is_top = False):
		self.func = func
		self.is_top = is_top

	def __str__(self):
		return '###%s %s(%s)\n\n%s' % (
			'' if self.is_top else '#',
			self.func.__name__,
			', '.join(
				inspect.getargspec(self.func).args if self.is_top
				else inspect.getargspec(self.func).args[1:]
			),
			util.gen_tables(
				textwrap.dedent(
					self.func.__doc__
				).strip()
			).strip()
		)

class Class(object):
	'''
	A class

	Args:
		obj (type): The object to wrap
	'''

	def __init__(self, obj):
		self.obj = obj
		self.funcs = []

		for func in dir(obj):
			func = getattr(obj, func)

			try:
				if func.__module__ == obj.__module__:
					if func.__name__[0] is not '_':
						self.funcs.append(Function(func))
			except:
				pass

	def __str__(self):
		parent = inspect.getmro(self.obj)[1]
		if parent.__module__ is not 'builtins':
			parent = parent.__module__ + '.' + parent.__name__
		else:
			parent = parent.__name__

		result = '### %s(%s)\n\n%s' % (
			self.obj.__name__,
			parent,
			util.gen_tables(
				textwrap.dedent(
					self.obj.__doc__
				).strip()
			).strip()
		)

		if len(self.funcs) > 0:
			result += '\n\n%s' % (
				'\n\n'.join(str(func) for func in self.funcs)
			)

		return result

class Module(object):
	'''
	A module

	Args:
		mod (module): The module to wrap
		pkg (str): The location of the module
	'''

	def __init__(self, mod, pkg):
		self.mod = mod
		self.pkg = pkg
		self.name = mod.__name__.split('.')[-1].title()
		self.docs = mod.__doc__.strip()
		self.objs = []
		self.funcs = []

		for name, mem in inspect.getmembers(self.mod):
			if hasattr(mem, '__module__'):
				if self.mod.__name__ is mem.__module__:
					if mem.__name__[0] is not '_':
						if inspect.isclass(mem):
							self.objs.append(Class(mem))
						elif inspect.isfunction(mem):
							self.funcs.append(Function(mem, True))

	def __str__(self):
		result = '%s\n%s\n\n%s\n\n%s' % (
			self.name,
			'=' * len(self.name),
			self.docs,
			('- ' * 40).strip()
		)

		if len(self.objs) > 0:
			result += '\n\n**Classes:**\n------------\n\n%s' % (
				'\n\n\n'.join(str(obj) for obj in self.objs)
			)

		if len(self.funcs) > 0:
			result += '\n\n**Functions:**\n--------------\n\n%s' % (
				'\n\n\n'.join(str(func) for func in self.funcs)
			)

		return result

	def save(self):
		'''
		Saves the generated documentation

		Returns:
			A string containing the location of the module
		'''

		pkg_path = self.mod.__name__.split('.')
		file_name = pkg_path[-1] + '.md'
		file_path = os.path.join(
			os.getcwd(),
			'docs',
			*pkg_path[1:-1]
		)
		full_path = os.path.join(file_path, file_name)

		if not os.path.isdir(file_path):
			os.makedirs(file_path)

		with open(full_path, 'w') as f:
			f.write(str(self))
			f.write('\n')

		return self.mod.__name__

class Package(object):
	'''
	A package

	Args:
		pkg (str): The name of the package to import
	'''

	def __init__(self, pkg):
		self.pkg = __import__(pkg, fromlist = [])
		self.mods = []

		mods = __import__(pkg, fromlist = self.pkg.__all__)
		for attr in dir(mods):
			if not attr.endswith('__'):
				self._get_modules(mods, attr, pkg)

	def __str__(self):
		return '\n\n\n\n\n'.join(str(mod) for mod in self.mods)

	def _get_modules(self, mods, mod, pkg):
		'''
		Recursively locates modules in the package

		Args:
			mods (module): The module to process
			mod (str): The name of the module
			pkg (str): The name of the package
		'''

		try:
			mod = __import__(
				pkg + '.' + mod,
				fromlist = getattr(mods, mod).__all__
			)

			for attr in dir(mod):
				if not attr.endswith('__'):
					self._get_modules(mod, attr, mod.__package__)
		except:
			try:
				mod = __import__(
					pkg + '.' + mod,
					fromlist = [mod]
				)

				self.mods.append(
					Module(mod, pkg)
				)
			except:
				pass

	def save(self):
		'''
		Recursively saves the generated documentation

		Returns:
			A tuple of the modules saved
		'''

		result = ()

		for mod in self.mods:
			result += (mod.save(),)

		return result
