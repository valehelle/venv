from django.conf import settings
from django.db import models
from time import time
import datetime
import uuid
from sorl.thumbnail import ImageField

# Create your models here.
#Return the name to the Image file.
def get_upload_file_name(instance,filename):
	return "media/" + str(instance.username) + "/%s_%s" % (str(time()).replace('.','_'),filename)


# User can have multiple story
class Story(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL)
	datetime = models.DateTimeField(auto_now_add=True, blank=False)
	star = models.IntegerField(null=True)
	title = models.CharField(max_length = 200)
	storyid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
	
#Text will be inside story
class Text(models.Model):
	id = models.AutoField(primary_key=True)
	text = models.CharField(max_length = 200)
	position = models.IntegerField(default = 0)
	storyid = models.UUIDField(default=uuid.uuid4)
	username = models.CharField(max_length = 50)
	
	
	
#Item will be inside story
class Image(models.Model):
	source = models.FileField(upload_to = get_upload_file_name)
	position = models.IntegerField(default = 0)
	storyid = models.UUIDField(default=uuid.uuid4)
	username = models.CharField(max_length = 50)
