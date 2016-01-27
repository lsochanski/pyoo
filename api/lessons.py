from ast import ClassDef, FunctionDef, Print, Import, ImportFrom, alias

class Error(object):
	@staticmethod
	def create(message, node):
		error_dict = { 'msg': message }
		if hasattr(node, 'line'):
			error_dict['line_no': node.lineno]
		if hasattr(node, 'col_offset'):
			error_dict['col': node.col_offset]
		return error_dict

class OOLessons(object):
	@staticmethod
	def lesson1(node):
		""" Tests if code contains 'import time' """
		response = { 'success': False, 'errors': []}
		import_statement_found = False
		time_import_found = False
		if not hasattr(node, 'body'):
			response['errors'].append(
				Error.create("Code doesn't have body.", node)
			)
		for body_node in node.body:
			if not isinstance(body_node, Import):
				continue
			import_statement_found = True
			if not len(node.body) > 0 or not hasattr(body_node, 'names') or not len(body_node.names) is 1:
				continue;
			if (body_node.names[0].name is 'time'):
				response['success'] = True
				time_import_found = True
		if not import_statement_found:
			response['errors'].append(
				Error.create("You have to use 'import' statement.", node)
			)
		if not time_import_found and import_statement_found:
			response['errors'].append(
				Error.create('Wrong module.', node)
			)
		return response

	@staticmethod
	def lesson2(node):
		""" Tests if code contains 'from garage import car' """
		response = { 'success': False, 'errors': []}
		import_from_statement_found = False
		time_import_found = False
		if not hasattr(node, 'body'):
			response['errors'].append(
				Error.create("Code doesn't have body.", node)
			)
		for body_node in node.body:
			if not isinstance(body_node, ImportFrom):
				continue
			import_from_statement_found = True
			for alias_name in body_node:
				if not isinstance(alias_name, alias):
					continue
				if not alias_name.name is 'car':
					response['errors'].append(
						Error.create(
							"You have to import 'car', not '{name}'."
							.format(name=alias_name.name), 
							body_node
						)
					)

			
		if not import_from_statement_found:
			response['errors'].append(
				Error.create("You have to use 'from ... import ...' statement.", node)
			)
		return response