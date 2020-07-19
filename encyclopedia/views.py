from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponseNotFound
from django.shortcuts import redirect

import random
from . import util
import markdown

def index(request):
	return render(request, "encyclopedia/index.html", { "title": "All Pages", "entries": util.list_entries()})

def create(request):
	if request.method=="POST":
		data=request.POST.copy()
		topic=data.get('topic')
		content=data.get('content')
		edit=str(data.get('edit'))

		if util.get_entry(topic) is None:
			content='# '+topic+"\r\n"+content
			util.save_entry(topic, content)
			md=markdown.Markdown()
			entry=mark_safe(md.convert(util.get_entry(topic)))
			return render(request, "encyclopedia/topic.html",{ "entry": entry, "title": topic })
		
		elif edit=="yes":
			util.save_entry(topic, content)
			md=markdown.Markdown()
			entry=mark_safe(md.convert(util.get_entry(topic)))
			return render(request, "encyclopedia/topic.html",{ "entry": entry, "title": topic })

		else:
			return HttpResponseNotFound('<h1 style="margin-top: 0px;padding-top: 20px; margin-left: 20%; margin-bottom: 20px; border-bottom: solid;">Page Already exists...</h1>')

	else:
		return render(request, "encyclopedia/create.html",{ "topic": "", "content": ""})

def topic(request, title):
	if request.method=="POST":
		data=request.POST.copy()
		title=str(data.get('title'))

	md=markdown.Markdown()
	results=[]
	if util.get_entry(title) is None:
		for entry in util.list_entries():
			if title.lower() in entry.lower():
				results.append(entry)

		if len(results)==0:
			return HttpResponseNotFound('<h1 style="margin-top: 0px;padding-top: 20px; margin-left: 20%; margin-bottom: 20px; border-bottom: solid;">No Page Found</h1>')
		else:
			return render(request, "encyclopedia/index.html", { "title": "Pages Found", "entries": results})
			
	else:
		entry=mark_safe(md.convert(util.get_entry(title)))
		return render(request, "encyclopedia/topic.html",{ "entry": entry, "title": title })

def edit(request, title):
	return render(request, "encyclopedia/create.html",{ "topic": title, "content": util.get_entry(title)})

def rand(request):
	t=random.choice(util.list_entries())
	return redirect('topic', title=t)