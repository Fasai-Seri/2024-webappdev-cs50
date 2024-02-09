from django.shortcuts import render

from . import util
import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def show(request, entry):
    return render(request, "encyclopedia/show.html", {
        "entry": entry,
        "details": markdown2.markdown(util.get_entry(entry))
    })