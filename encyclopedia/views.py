from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import markdown2

class NewSearchForm(forms.Form):
    search = forms.CharField(label="Search")

# class NewPageForm(forms.Form):
#     title = forms.CharField(label="Title"),
#     te
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
    search = request.GET['search']
    print(search)
    if  search in util.list_entries():
        return render(request, "encyclopedia/search.html", {
            "test": search
        })
    
def create(request):
    return HttpResponseRedirect(reverse('encyclopedia:index'))
        


    
                