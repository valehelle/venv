from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory
from models import Story,Text,Image
from django.contrib.auth.models import User
from operator import attrgetter
from itertools import chain
from uuid import UUID

# Create your views here.
def create_stories(request):

	if request.user.is_authenticated():
		if request.POST:
			current_user = request.user
			#Get the form for all type
			storyform = StoryForm(request.POST,prefix = "Story")
			#Handle insertion for the title.
			if storyform.is_valid():
				story = storyform.save(commit = False)
				story.user_id = current_user.id
				story.save()
				#Handle insertion of the text		
				for f,p in zip(request.POST.getlist('text'),request.POST.getlist('text_position')):
					text = TextForm(request.POST)
					if text.is_valid():
						addtext = text.save(commit = False)
						addtext.storyid = story.storyid
						addtext.username = current_user.username
						addtext.position = p
						addtext.text = f
						addtext.save()
					else:
						return HttpRespondeRedirect('/TextInsertError')
				
				#Handle insertion of the image
				for f,p in zip(request.FILES.getlist('source'),request.POST.getlist('position')):
					form = ImageForm(request.POST, {'source': f})
					if form.is_valid():
						addimage = form.save(commit = False)
						addimage.storyid = story.storyid
						addimage.username = current_user.username
						addimage.position = p
						addimage.save()
					else:
						return HttpRespondeRedirect('/ImageInsertError')
			return HttpRespondeRedirect('/complete')
		else:
			imageform = ImageForm()
			textform = TextForm()
			storyform = StoryForm(prefix = "Story")
			args = {}
			args.update(csrf(request))
			args['textform'] = textform
			args['imageform'] = imageform
			args['storyform'] = storyform
			return render(request,"create_stories.html",args)
	else:
		return HttpRespondeRedirect("home.html")
		
		
def read_stories(request):
	if request.GET:
		#Get the story id from url.
		r_id = request.GET.get('s')
		try:
			val = UUID(r_id, version=4)
		except ValueError:
			# If it's a value error, then the string 
			# is not a valid hex code for a UUID.
			return HttpRespondeRedirect("/home")
			
		#Fetch the data necessary from database
		story = Story.objects.get(storyid = r_id)
		person = User.objects.get(id = story.user_id)
		image = Image.objects.filter(storyid = r_id)
		text = Text.objects.filter(storyid = r_id)
		#Combine result for text and image. Sort according to position
		combine = sorted(
						chain(text,image),
						key=attrgetter('position'))
		args = {}
		args['story'] = story
		args['items'] = combine
		args['author'] = person.username
		return render (request,"read_stories.html",args)
	else:
		return HttpRespondeRedirect("/home")
		