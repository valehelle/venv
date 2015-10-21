from django import forms
from models import Text,Image,Story 

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		exclude =("user","id","datetime","like","storyid")

class TextForm(forms.ModelForm):
	class Meta:
		model = Text
		exclude = ("storyid","username")
		
class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		exclude = ("storyid","username")