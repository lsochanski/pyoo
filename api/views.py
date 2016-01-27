import ast
from ast import ClassDef, FunctionDef, Print, ImportFrom
import json

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token
from django.contrib.auth.models import User as DjangoUser

from ast_validation.tools import is_class
from ast_validation.tools import does_class_name_match
from ast_validation.tools import Error

from .models import User
from .models import Lesson
from .models import TriedLesson

def get_last_tried_lesson(request):
	user = User.objects.get(django_user=request.user)
	# lesson = Lesson.objects.get(
	# 	id=TriedLesson.objects.get(user=)
	# )


# Create your views here.

def create_json_code_error(message, line_no, column_no):
	return {
		'type': 'code',
		'msg': message, 
		'line': int(line_no), 
		'col': int(column_no)
	}

def create_json_error(message):
	return {
		'type': 'all',
		'msg': message
	}


@csrf_exempt
def register(request):
	data = json.loads(request.body)
	django_user = DjangoUser.objects.create_user(
		data['name'], 
		data['mail'], 
		data['password']
	)
	User.register(django_user)

	return HttpResponse(json.dumps({'success': True}))


@csrf_exempt
def login(request):
	data = json.loads(request.body)
	django_user = DjangoUser.objects.get(
		username=data['name']
	)
	if not django_user.check_password(data['password']):
		return HttpResponse(json.dumps({'success': False}))
	# user = User.objects.get(django_user=django_user)
	# if not user:
	# 	return HttpResponse(json.dumps({'success': False}))
	return HttpResponse(json.dumps({'success': True, 'token': get_token(request)}))

@xframe_options_exempt
@csrf_exempt
def lesson_check(request, lesson_no):
	if not request.method == 'POST':
		return HttpResponse("")
		print 'here', lesson_no
	response = {}
	response['errors'] = []
	response['success'] = False
	try:
		parsed_body = json.loads(request.body)
		check_code(response, lesson_no, parsed_body['code'])
	except Exception as e:
		print e
	return HttpResponse(json.dumps(response))


def lesson_1(response, node):
	""" Tests if code contains 'import time' """
	
	if hasattr(node, 'body') and len(node.body) > 0:
		for body_node in node.body:
			if(hasattr(body_node, 'names') and len(body_node.names) is 1):
				if(body_node.names[0].name == 'time'):
					response['success'] = True
					return
				else:
					response['errors'].append(create_json_code_error('Module \'' + body_node.names[0].name + '\' is not the one you need.', body_node.lineno, body_node.col_offset))

		response['errors'].append(create_json_error('You have to "import time", there will be time to write more!'))
	else:
		response['errors'].append(create_json_error('Write something at least!'))


def lesson_2(response, node):
	""" Tests if code contains 'import time' """
	
	if hasattr(node, 'body') and len(node.body) > 0:
		for body_node in node.body:
			print body_node.__dict__

			if type(body_node) is ImportFrom:
				if body_node.module is 'car':
					for name in body_node.names:
						if name.name is 'engine':
							response['success'] = True
							return
				response['errors'].append(create_json_code_error('You have to import the \'engine\' module!', body_node.lineno, body_node.col_offset))
		response['errors'].append(create_json_error('You have to use \'from ... import ...\' statement!'))
		
	else:
		response['errors'].append(create_json_error('Write something at least!'))


def lesson_3(response, node):
	method_found = False
	if hasattr(node, 'body'):
		for body_node in node.body:
			if not is_class(body_node):
				continue
			if not does_class_name_match(body_node, 'Foo'):
				response['errors'].append(Error("Class should be named 'Foo'", body_node.lineno))
				return
			for class_body_node in body_node:
				if not isinstance(class_body_node, FunctionDef) or not hasattr(class_body_node, 'name'):
					continue
				if not class_body_node.name is 'bar':
					response['errors'].append(
						Error("The Foo class need no other methods than ", class_body_node.lineno)
					)
				method_found = True
				for method_body_node in class_body_node.body:
					if not isinstance(method_body_node, Print):
						response['errors'].append(
							Error(
								"Method 'bar' must contain only one instruction ('print').", 
								method_body_node.lineno
							)
						)
						return
					if not hasattr(method_body_node, 'values') or len(method_body_node.values) > 1:
						response['errors'].append(
							Error(
								"print instruction must have only one argument value", 
								method_body_node.lineno
							)
						)
						return
					if not method_body_node.values[0].s is 'hello':
						response['errors'].append(
							Error(
								"print instruction must say 'hello'", 
								method_body_node.values[0].lineno
							)
						)
						return

				# validate method
			if not method_found:
				response['errors'].append(Error("Class must contain the 'bar' method."))
				return
	else:
		response['errors'].append(create_json_error('Write something at least!'))


switch = {}
switch[str(1)] = lesson_1
switch[str(2)] = lesson_2
switch[str(3)] = lesson_3

def check_code(response, lesson_no, code):

	try:
		node = ast.parse(code)
		
		switch[str(lesson_no)](response, node)
	except TypeError as e:
		response['errors'].append(create_json_error(str(e)))
	except SyntaxError as e:
		response['errors'].append(create_json_code_error("Invalid syntax: " + e.text, e.lineno, e.offset))
	except Exception as e:
		response['errors'].append(create_json_error("Unknown: " + e.text))

