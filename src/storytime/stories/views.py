from django.shortcuts import render
from forms import ItemForm
from django.template.context_processors import csrf
from django.forms.formsets import formset_factory

# Create your views here.
def create_stories(request):
	if request.POST:
		for f in request.FILES.getlist('i_path'):
			print request.FILES
			form = ItemForm(request.POST, {'i_path': f})
			if form.is_valid():
				form.save()
		
		return HttpRespondeRedirect('/complete')
	else:
		form = ItemForm()
		args = {}
		args.update(csrf(request))
		args['form'] = form
		return render(request,"create_stories.html",args)