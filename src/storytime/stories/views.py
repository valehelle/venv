from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory

# Create your views here.
def create_stories(request):
	if request.user.is_authenticated():
		if request.POST:
			current_user = request.user
			position = 1
			#Get the form for all type
			imageform = ImageForm(request.POST,prefix = "Image")
			textform = TextForm(request.POST,prefix = "Text")
			storyform = StoryForm(request.POST,prefix = "Story")
			#Check if there is a title
			if storyform.is_valid():
				story = storyform.save(commit = False)
				story.user_id = current_user.id
				story.save()
				
			for f in request.FILES.getlist('source'):
				form = ImageForm(request.POST, {'source': f})
				if form.is_valid():
					addform = form.save(commit = False)
					addform.position = position
					addform.storyid_id = story.id
					addform.save()
					position = position + 1
				else:
					return HttpRespondeRedirect('/error')
			return HttpRespondeRedirect('/complete')
		else:
			imageform = ImageForm(prefix = "Image")
			textform = TextForm(prefix = "Text")
			storyform = StoryForm(prefix = "Story")
			args = {}
			args.update(csrf(request))
			args['textform'] = textform
			args['imageform'] = imageform
			args['storyform'] = storyform
			return render(request,"create_stories.html",args)
	else:
		return render(request,"home.html")