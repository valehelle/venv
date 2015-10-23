from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory
from models import Story,Text,Image
from operator import attrgetter
from itertools import chain

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
						addtext.storyid_id = story.id
						addtext.username = current_user.username
						addtext.position = p
						addtext.text = f
						addtext.save()
					else:
						return HttpRespondeRedirect('/TextInsertError')
				
				#Handle insertion of the image
				#Get the order of position first

				for f,p in zip(request.FILES.getlist('source'),request.POST.getlist('position')):
					form = ImageForm(request.POST, {'source': f})
					if form.is_valid():
						addimage = form.save(commit = False)
						addimage.storyid_id = story.id
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
		storyid = request.GET.get('s')
		#Fetch the data necessary from database
		story = Story.objects.get(id = storyid)
		image = Image.objects.filter(storyid_id = storyid)
		text = Text.objects.filter(storyid_id = storyid)
		#Combine result for text and image. Sort according to position
		combine = sorted(
						chain(text,image),
						key=attrgetter('position'))
		args = {}
		args['story'] = story
		args['items'] = combine
		return render (request,"read_stories.html",args)
	else:
		return HttpRespondeRedirect("/home")