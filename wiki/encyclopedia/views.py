from django.shortcuts import render
from . import util
import re
import markdown2
import random
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.
class NewPageForm(forms.Form):
    page_entry=forms.CharField(widget=forms.Textarea, label="Create New Page")

class NewTitleForm(forms.Form):
    page_title = forms.CharField(label="Enter Title")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content=convert(title)
    heading=re.search(title, content, re.IGNORECASE)
    if content == None:
        return render(request, "encyclopedia/error.html")
    return render(request, "encyclopedia/entry.html", {"content":content, "title": heading[0]})
    

def search(request):
    total_entries=util.list_entries()
    query = request.GET.get('q')
    results=[]
    for entry in total_entries:
        if re.search(query, entry, re.IGNORECASE):
            results.append(entry)
            rg=f"^{query}$"
            raw= r'{}'.format(rg)
            if re.search(raw, entry, re.IGNORECASE):
                content=util.get_entry(entry)
                return render(request, "encyclopedia/entry.html", {"content":content, "title": entry.upper()})
    return render(request, "encyclopedia/search.html", {"results":results, "query":query, "res":len(results)!=0})

def new_page(request):
    if request.method == "POST":
        t_form = NewTitleForm(request.POST)
        c_form = NewPageForm(request.POST)
        if c_form.is_valid() and t_form.is_valid():
            content = c_form.cleaned_data["page_entry"]
            title = t_form.cleaned_data["page_title"]
            if title not in util.list_entries():
                util.save_entry(title, content)
                return render(request, "encyclopedia/entry.html", {"content":content, "title": title.upper()})
            else:
                return render(request, "encyclopedia/create.html", {"red": True})
        else:
            return render(request, "encyclopedia/create.html", {"textarea": NewPageForm(), "title": NewTitleForm()})
    return render(request, "encyclopedia/create.html", {
        "textarea": NewPageForm(),
        "title": NewTitleForm(),
        "red": None,
        })

def edit_page(request, title):
    content=convert(title)
    if request.method == "POST":
        new_content = request.POST.get("content")
        util.save_entry(title, new_content)
        return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))
    return render(request, "encyclopedia/edit.html", {"title":title, "content":content})

def random_page(request):
    total_entries=util.list_entries()
    total=len(total_entries)
    lucky_num = random.randrange(total)
    title = total_entries[lucky_num]
    return HttpResponseRedirect(reverse("encyclopedia:entry", kwargs={'title': title}))

def convert(title):
    content=util.get_entry(title)
    converted = markdown2.markdown(content)
    return converted