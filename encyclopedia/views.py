from django.shortcuts import render
import markdown2
from . import util
from .forms import EditEntry, CreateEntry
import random


def edit(request, entry):
    form = EditEntry()
    return render(request, "encyclopedia/edit.html", {
        # "entry": entry,
        "title": entry,
        "form": form
    })


def create(request, entry):
    entry = CreateEntry()
    # form = CreateEntry()
    return render(request, "encyclopedia/create.html", {
       "form": entry
    })


def index(request):
    if request.POST.get('q') == None:
        return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
        })
        search(request, str(request.POST.get('q')))
    else:
        entry = str(request.POST.get('q'))
        list = util.list_entries()
        results = []
        for i in list:
            if entry.lower() in i.lower():
                results.append(i)
        if results == []:
            return render(request, "encyclopedia/not_found.html", {"entry": entry})
        return render(request, "encyclopedia/search.html", {"results": results, "title": entry})


def show(request, entry):
    article = util.get_entry(entry)
    if article is None:
        return render(request, "encyclopedia/not_found.html", {"entry": entry, "title": entry})
    else:
        article_html = markdown2.markdown(article)
        return render(request, "encyclopedia/show.html", {"entry": article_html, "title": entry})


def save(request, entry):
    if entry in util.list_entries():
        title = entry
    else:
        title = request.POST["title"]
    content = request.POST["content"]
    util.save_entry(title, content)
    return show(request, title)


def randomize(request):
    page = random.choice(util.list_entries())
    return show(request, page)