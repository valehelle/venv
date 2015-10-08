from django.db import models
from time import time
# Create your models here.
#Return the name to the Image file.
def get_upload_file_name(instance,filename):
	return "uploaded_files/%s_%s" % (str(time()).replace('.','_'),filename)


#Item will be inside story
class Item(models.Model):
	i_name = models.CharField(max_length = 30)
	i_path = models.FileField(upload_to = get_upload_file_name)