from django import forms
from models import Text,Image,Story,User_Info

class StoryForm(forms.ModelForm):
	class Meta:
		model = Story
		exclude =("user","id","datetime","like","storyid","starcount","complete")

class TextForm(forms.ModelForm):
	class Meta:
		model = Text
		exclude = ("storyid","username","textid")
		
class ImageForm(forms.ModelForm):
	class Meta:
		model = Image
		exclude = ("storyid","username","imageid")
		
class EditForm(forms.ModelForm):
	class Meta:
		model = User_Info
		exclude = ("profile_pic","user")
		
class EditFormImage(forms.ModelForm):
	class Meta:
		model = User_Info
		exclude = ("user","desc","username")