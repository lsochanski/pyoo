import ast

from django.test import TestCase

from lessons import OOLessons

class LessonsTestCase(TestCase):
    def setUp(self):
        pass

    def test_lesson_1(self):
        """Animals that can speak are correctly identified"""
        self.assertIsInstance(
        	OOLessons.lesson1(ast.parse("")), 
        	dict
        )
        self.assertEqual(
        	OOLessons.lesson1(ast.parse("")),
        	{ 'success': False, 'errors': [{ 'msg': "You have to use 'import' statement."}]}
        )
        self.assertEqual(
        	OOLessons.lesson1(ast.parse("""import wrong_module""")), 
        	{ 'success': False, 'errors': [{ 'msg': 'Wrong module.'}]}
        )
        self.assertEqual(
        	OOLessons.lesson1(ast.parse("""\nimport bla\nimport ble\nclass Foo:\tpass""")), 
        	{ 'success': False, 'errors': [ { 'msg': 'Wrong module.'}]}
        )


        self.assertEqual(
        	OOLessons.lesson1(ast.parse("""import time\n""")), 
        	{ 'success': True, 'errors': []}
        )
        self.assertEqual(
        	OOLessons.lesson1(ast.parse("""\n\nimport time\n""")), 
        	{ 'success': True, 'errors': []}
        )
        self.assertEqual(
        	OOLessons.lesson1(ast.parse("""\nimport bla\nimport time\nclass Foo:\tpass""")), 
        	{ 'success': True, 'errors': []}
        )

    def test_lesson_2(self):
    	self.assertIsInstance(
        	OOLessons.lesson2(ast.parse("")), 
        	dict
        )
        self.assertEqual(
        	OOLessons.lesson2(ast.parse("")),
        	{ 'success': False, 'errors': [{ 'msg': "You have to use 'import ... from ...' statement."}]}
        )
        self.assertEqual(
        	OOLessons.lesson2(ast.parse("")),
        	{ 'success': False, 'errors': [
        	{ 'msg': "You have to import 'car', not '{name}'.", }]}
        )
        # self.assertEqual(
        # 	OOLessons.lesson2(ast.parse("from garage import car")),
        # 	{ 'success': True, 'errors': []}
        # )


