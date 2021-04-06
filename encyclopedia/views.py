from django.shortcuts import render, redirect
import markdown2
from . import util
from .forms import EditEntry, CreateEntry
import random


def edit(request, entry):
    form = EditEntry()
    return render(request, "encyclopedia/edit.html", {
        "title": entry,
        "form": form
    })


def create(request):
    entry = CreateEntry()
    return render(request, "encyclopedia/create.html", {
       "form": entry
    })


def index(request):
    if request.method == 'POST':
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
                if entry.lower() == i.lower():
                    print(f'founded {i}')

                    return redirect(f'/wiki/{i}')
                    # break
                elif entry.lower() in i.lower():
                    results.append(i)
            if not results:
                return render(request, "encyclopedia/not_found.html", {"entry": entry})
            # print(results)
            return render(request, "encyclopedia/search.html", {"results": results, "title": entry})

    return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })


def show(request, entry):
    if request.method == "POST":
        if request.POST.get('q') is None:
            return render(request, "encyclopedia/index.html", {
                "entries": util.list_entries()
            })
            search(request, str(request.POST.get('q')))
        else:
            entri = str(request.POST.get('q'))
            list = util.list_entries()
            results = []
            for i in list:
                if entri.lower() == i.lower():
                    print(f'founded {i}')
                    return redirect(f'/wiki/{i}')
                    # break
                elif entri.lower() in i.lower():
                    results.append(i)
            if results == []:
                return render(request, "encyclopedia/not_found.html", {"entry": entri})
        return render(request, "encyclopedia/search.html", {"results": results, "title": entri})
    article = util.get_entry(entry)
    print(entry)
    print(f'article: {entry}')
    if article is None:
        return render(request, "encyclopedia/not_found.html", {"entry": entry, "title": entry})
    else:
        article_html = markdown2.markdown(article)
        return render(request, "encyclopedia/show.html", {"entry": article_html, "title": entry})


def save(request, entry):
    if request.method == 'POST':
        title = request.POST["title"]
        for entri in util.list_entries():
            if title.lower() == entri.lower():
                return render(request, "encyclopedia/alreadyexists.html", {"entry": entri})
        content = request.POST["content"]
        util.save_entry(title, content)
        return show(request, title)


def save_edited(request, entry):
    if request.method == 'POST':
        title = entry
        content = request.POST["content"]
        util.save_entry(title, content)
        return show(request, title)


def randomize(request):
    page = random.choice(util.list_entries())
    return show(request, page)
