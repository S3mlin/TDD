from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from lists.models import Item, List
from lists.forms import ItemForm

# Create your views here.
def home_page(request):
    current_user = request.user
    print(current_user)
    return render(request, 'home.html', {"form": ItemForm(), "user": current_user})


def view_list(request, list_id):
    our_list = List.objects.get(id=list_id)
    if request.method == "POST":
        form = ItemForm(data=request.POST)
        if form.is_valid():
            form.save(for_list=our_list)
            return redirect(our_list)
    else:
        form = ItemForm()
    return render(request, "list.html", {"list": our_list, "form": form})


def new_list(request):
    form = ItemForm(data=request.POST)
    if form.is_valid():
        nulist = List.objects.create()
        form.save(for_list=nulist)
        return redirect(nulist)
    else:
        return render(request, "home.html", {"form": form})
    

def my_lists(request, email):
    return render(request, 'my_lists.html')