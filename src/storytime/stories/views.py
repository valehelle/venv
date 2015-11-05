from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory
from models import Story,Text,Image,Person,RELATIONSHIP_FOLLOWING
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.views import login


def custom_login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect("/following/")
    else:
        return login(request)
		
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
					if f.size > 5000000:
						from django.contrib import messages
						messages.add_message(request, messages.WARNING, 'Image size should not be more than 5MB.')
						return render_page(request,"create_stories.html","custom error")
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
		
#Render page. This is for create_stories
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
	

#Read a specific story given the url.
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
	
#Show story from people who you followed	
def following(request):
	if request.user.is_authenticated():
		return render (request,"following.html",[])
	else:
		return HttpResponseRedirect("/accounts/login/")

#Show the user profile given the url
def user_profile(request):
	if request.user.is_authenticated():
		if request.GET:
			name = request.GET.get('u')
			#Get the person from the username
			person = User.objects.get(username=name)
			#Count number of story
			stories = Story.objects.filter(user_id = person.id)
			storycount = stories.count()
			#Get the first image of the story
			imagelist = []
			for story in stories:
				#Get the first image of every story and append to image list.
				image = Image.objects.filter(storyid = story.storyid).first()
				imagelist.append(image)
				
			list = zip(stories,imagelist)
			#Get the person object from the username
			profileuser = Person.objects.get(name = person.username)
			#Get the user following and follower
			followers = profileuser.get_followers()
			followingcount = profileuser.get_following().count()
			followercount = profileuser.get_followers().count()

			#Determine whether the user is looking at his/her own profile
			item = ""
			if person.id == request.user.id :
				item = "User"
			else:
				try:
					followers.get(name = request.user.username)
					item = "Unfollow"
				except :
					item = "Follow"
				
			args = {}
			args.update(csrf(request))
			args['storycount'] = storycount
			args['list'] = list
			args['followingcount'] = followingcount
			args['followerscount'] = followercount
			args['user'] = person
			args['item'] = item
		return render (request,"user_profile.html",args)
	else:
		return HttpResponseRedirect("/accounts/login/")
		
#Handle unfollow request	
def unfollow(request):
	if request.POST:
		#Get the username for the user and the person he/she want to unfollow
		person = request.POST.get("username")
		user = request.user.username
		#Get the person object for both of the person
		profileuser,profilecreated = Person.objects.get_or_create(name = person)
		user,usercreated = Person.objects.get_or_create(name = user)
		#Remove their relationship
		user.remove_relationship(profileuser,RELATIONSHIP_FOLLOWING)
		import json
		data = {}
		data['string'] = '<button type="button" class="btn btn-success item" id = "follow" value = " ' + person + ' ">Follow</button>'
		return HttpResponse(json.dumps(data), content_type = "application/json")
#Handle unfollow request	
def follow(request):
	if request.POST:
		#Get the username for the user and the person he/she want to unfollow
		person = request.POST.get("username")
		user = request.user.username
		#Get the person object for both of the person
		profileuser,profilecreated   = Person.objects.get_or_create(name = person)
		user,usercreated = Person.objects.get_or_create(name = user)
		#Remove their relationship
		user.add_relationship(profileuser,RELATIONSHIP_FOLLOWING)
		import json
		data = {}
		data['string'] = '<button type="button" class="btn btn-success item" id = "unfollow" value = " ' + person + ' ">Unfollow</button>'
		return HttpResponse(json.dumps(data), content_type = "application/json")

