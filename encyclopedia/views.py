from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from . import util
import markdown2
import random


class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title")
    details = forms.CharField(widget=forms.Textarea())
    
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def show(request, entry):
    return render(request, "encyclopedia/show.html", {
        "entry": entry,
        "details": markdown2.markdown(util.get_entry(entry)),
        "form": NewSearchForm(),
    })
    
def search(request):
    existing = util.list_entries()
    search = request.GET['search']
    if search.lower() in [entry.lower() for entry in existing]:
        return HttpResponseRedirect(reverse('show', args=[search]))
    else:
        find = [entry for entry in existing if search.lower() in entry.lower()]
        return render(request, 'encyclopedia/search.html', {
            "entries": find,
            "form": NewSearchForm()
        })

def create(request, exist=[entry.lower() for entry in util.list_entries()]):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            details = form.cleaned_data["details"]
            if title.lower() in exist:
                return render(request, "encyclopedia/create.html", {
                "form": NewSearchForm(),
                "page": form,
                "error": 'This title is already existed'
            })
            else:
                util.save_entry(title, details)
                return HttpResponseRedirect(reverse('show', args=[title]))
        else:
            return render(request, "encyclopedia/create.html", {
                "form": NewSearchForm(),
                "page": form,
                "error": 'The form is not valid'
            })
    else:
        return render(request, "encyclopedia/create.html",{
            "form": NewSearchForm(),
            "page": NewPageForm()
        })
    
def edit(request, entry):
    if request.method == "POST":
        update = request.POST['update']
        util.save_entry(entry, update)
        return HttpResponseRedirect(reverse('show', args=[entry]))
    else:
        return render(request, "encyclopedia/edit.html", {
            "entry": entry,
            "details": markdown2.markdown(util.get_entry(entry))
        })
        
def random_page(request):
    exist = util.list_entries()
    result = random.choice(exist)
    return HttpResponseRedirect(reverse('show', args=[result]))