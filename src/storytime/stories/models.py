from django.conf import settings
from django.db import models
from time import time
import datetime


# Create your models here.
#Return the name to the Image file.
def get_upload_file_name(instance,filename):
	return "media/" + str(instance.username) + "/%s_%s" % (str(time()).replace('.','_'),filename)


# User can have multiple story
class Story(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	datetime = models.DateTimeField(auto_now_add=True, blank=False)
	like = models.IntegerField(null=True)
	title = models.CharField(max_length = 140)
	
#Text will be inside story
class Text(models.Model):
	text = models.CharField(max_length = 140)
	position = models.IntegerField()
	storyid = models.ForeignKey(Story)
	username = models.CharField(max_length = 50)
	
#Item will be inside story
class Image(models.Model):
	source = models.FileField(upload_to = get_upload_file_name)
	position = models.IntegerField()
	storyid = models.ForeignKey(Story)
	username = models.CharField(max_length = 50)
