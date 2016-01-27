from django.db import models
from django.contrib.auth.models import User as DjangoUser



# Create your models here.
class Lesson(models.Model):
	title = models.CharField(max_length=256)
	contents = models.CharField(max_length=2048)
	number = models.IntegerField(default=0)


class User(models.Model):
	django_user = models.OneToOneField(DjangoUser)
	tried_lessons = models.ManyToManyField(Lesson, through='TriedLesson')

	@staticmethod
	def register(django_user):
		user = User(django_user=django_user)
		user.save()




class TriedLesson(models.Model):
	user = models.ForeignKey(User)
	lesson = models.ForeignKey(Lesson)
	time = models.DateTimeField(auto_now_add=True)
	tries = models.IntegerField(default=0)
	is_done = models.BooleanField(default=False)
	code_state = models.CharField(max_length=4096)




