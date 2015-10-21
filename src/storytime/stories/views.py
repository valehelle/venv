from django.shortcuts import render
from forms import TextForm,ImageForm,StoryForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory

# Create your views here.
def create_stories(request):
	
	if request.user.is_authenticated():
		if request.POST:
			print request.POST
			current_user = request.user
			position = 1
			#Get the form for all type
			textform = TextForm(request.POST,prefix = "Text")
			storyform = StoryForm(request.POST,prefix = "Story")
			#Handle insertion for the title.
			if storyform.is_valid():
				story = storyform.save(commit = False)
				story.user_id = current_user.id
				story.save()
				#Handle insertion of the text
				if textform.is_valid():
					addtext = textform.save(commit = False)
					addtext.storyid_id = story.id
					addtext.username = current_user.username
					addtext.save()
					position = position + 1
				
				#Handle insertion of the image
				#Get the order of position first

				for p,f in zip(request.POST.getlist('position'),request.FILES.getlist('source')):
					form = ImageForm(request.POST, {'source': f})
					if form.is_valid():
						addimage = form.save(commit = False)
						addimage.storyid_id = story.id
						addimage.username = current_user.username
						addimage.position = p
						addimage.save()
						position = position + 1
					else:
						return HttpRespondeRedirect('/error')
			return HttpRespondeRedirect('/complete')
		else:
			imageform = ImageForm()
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