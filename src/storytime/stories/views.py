from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory
from models import Story,Text,Image,Person,RELATIONSHIP_FOLLOWING
from django.contrib.auth.models import User



# Create your views here.
def create_stories(request):
	if request.user.is_authenticated():
		if request.POST:
			current_user = request.user
			list_form = []
			#Get the story form
			storyform = StoryForm(request.POST,prefix = "Story")
			#Check if text and image exists
			if not (request.POST.getlist('text') and request.FILES.getlist('source')):
				from django.contrib import messages
				messages.add_message(request, messages.WARNING, 'Please insert at least 1 text and 1 image')
				return render_page(request,"create_stories.html","custom error")
				
			#Handle insertion for the title.
			if storyform.is_valid():
				story = storyform.save(commit = False)
				story.user_id = current_user.id
				list_form.append(story)
				#Handle insertion of the text
				for f,p in zip(request.POST.getlist('text'),request.POST.getlist('text_position')):
					text = TextForm(request.POST,{'position' : p,'text': f })
					if text.is_valid():
						addtext = text.save(commit = False)
						addtext.storyid = story.storyid
						addtext.username = current_user.username
						addtext.position = p
						addtext.text = f
						list_form.append(addtext);
					else:
						return render_page(request,"create_stories.html",{'form': text})


				#Handle insertion of the image
				for f,p in zip(request.FILES.getlist('source'),request.POST.getlist('position')):
					form = ImageForm(request.POST, {'source': f })
					if form.is_valid():
						addimage = form.save(commit = False)
						addimage.storyid = story.storyid
						addimage.username = current_user.username
						addimage.position = p
						list_form.append(addimage);
					else:
						return render_page(request,"create_stories.html",{'form': form})
				for item_form in list_form:
					item_form.save()
				return HttpRespondeRedirect('/complete')
			else:
				return render_page(request,"create_stories.html",{'form': storyform})
		else:
			return render_page(request,"create_stories.html","no error")
	else:
		return HttpRespondeRedirect("home.html")
		
def render_page(request,html,form):
	#Create all the form required for the page
	imageform = ImageForm()
	textform = TextForm()
	storyform = StoryForm(prefix = "Story")
	args = {}
	#Add csrf security
	args.update(csrf(request))
	args['textform'] = textform
	args['imageform'] = imageform
	args['storyform'] = storyform
	
	#if there is an error add it inside the args
	if isinstance(form, dict):
		args['form'] = form['form']
	#Render the page with the args.
	return render(request,html,args)
	
def testing(request):
	if request.GET:
		r_id = request.GET.get('u')
		usering = request.user
		person = User.objects.get(id = usering.id)
		person2 = User.objects.get(id = r_id)
		user = Person.objects.get(name = person.username)
		user2 = Person.objects.get(name = person2.username)
		user3 = user.get_following().filter(name = 'hello')

		print user3
		
	return render (request,"read_stories.html",[])

	
def read_stories(request):
	#Import library needed
	from uuid import UUID
	from operator import attrgetter
	from itertools import chain
	
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
		