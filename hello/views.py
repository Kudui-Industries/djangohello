import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from numpy.ma.core import less_equal

from .forms import ImageUploadForm
from .forms import AddToInventory
from hello.models import Task
from hello.models import Inventory
from hello.models import Item
from django.db.models import Min
from django.db.models import Q

ENV = os.environ.get('ENV', 'dev')

@csrf_exempt
def index(request):
    context = {
        "title": "Index Page"

    }
    return render(request, "magazyn/index.html", context=context)

def hello_world(request):
    try:
        # Spróbuj pobrać wszystkie zadania z bazy danych
        tasks = Task.objects.all()
        task_list = "<br>".join([f"{task.id}. {task.title}" for task in tasks])
        db_status = "Połączenie z bazą danych działa poprawnie!"
    except Exception as e:
        # Jeśli pojawi się błąd, zapisz komunikat
        task_list = ""
        db_status = f"Błąd bazy danych: {str(e)}"

    # Formularz do dodawania zadań
    if request.method == 'POST':
        try:
            title = request.POST.get('title', '')
            description = request.POST.get('description', '')
            if title:
                Task.objects.create(title=title, description=description)
                return redirect('hello_world')  # Zakładając, że ten widok ma nazwę URL 'hello_world'
        except Exception as e:
            db_status += f"<br>Błąd podczas dodawania zadania: {str(e)}"

    # HTML z formularzem i listą zadań
    form_html = """
    <form method="post">
      <div>
        <label for="title">Tytuł zadania:</label>
        <input type="text" id="title" name="title" required>
      </div>
      <div>
        <label for="description">Opis:</label>
        <textarea id="description" name="description"></textarea>
      </div>
      <button type="submit">Dodaj zadanie</button>
    </form>
    """

    return HttpResponse(f"""
    <h1>Hello, World!</h1>
    <p>Środowisko: {ENV}</p>
    <p>Status bazy danych: {db_status}</p>
    <h2>Dodaj nowe zadanie:</h2>
    {form_html}
    <h2>Lista zadań:</h2>
    <p>{task_list if task_list else "Brak zadań"}</p>
    """)

def inventory_list(request):
    inventorys = Inventory.objects.all()
    sort_by = request.GET.get('sort_by', 'expiry_date')  # Default to sorting by 'expiry date':
    sort_dir = request.GET.get('sort_direction', 'asc')  # Default to direction ascending
    if sort_dir == "asc":
        ordering = sort_by
    else:
        if sort_dir == "desc":
            ordering = "-" + sort_by

    inventorys = Inventory.objects.all().order_by(ordering)
    context = {
        "title": "inventory List",
        'inventorys': inventorys
    }
    return render(request, 'magazyn/inventory_list.html', {'inventorys': inventorys, 'sort_by': sort_by})

def gtin_inventory_list(request,pk):
    sort_by = request.GET.get('sort_by', 'expiry_date')  # Default to sorting by 'expiry date':
    sort_dir = request.GET.get('sort_direction', 'asc')  # Default to direction ascending
    if sort_dir == "asc":
        ordering = sort_by
    else:
        if sort_dir == "desc":
            ordering = "-" + sort_by

    inventorys = Inventory.objects.filter(gtin=pk).order_by(ordering)
    context = {
        "title": "inventory List",
        'inventorys': inventorys
    }
    return render(request, 'magazyn/inventory_list.html', {'inventorys': inventorys, 'sort_by': sort_by})

def product_details_view(request,pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context={
        'inventory': inventory
    }
    return render(request, "magazyn/product_details.html", context= context)

def item_list(request):
    items = Item.objects.all()
    sort_by = request.GET.get('sort_by', 'name')  # Default to sorting by 'name':
    sort_dir = request.GET.get('sort_direction', 'asc')  # Default to direction ascending
    if sort_dir == "asc":
        ordering = sort_by
    else:
        if sort_dir == "desc":
            ordering = "-" + sort_by

    if sort_by == 'expiry_date':
        # Filter out items with expiry_date == None or == 9999-12-31
        items = Item.objects.exclude(Q(count=0)).order_by(ordering)
    else:
        items = Item.objects.all().order_by(ordering)
    context = {
        "title": "Item List",
        'items': items
    }
    return render(request, 'magazyn/item_list.html', {'items': items, 'sort_by': sort_by})


def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save_and_to_new':
                return redirect('upload_image')  # adjust name as needed
            else:
                return redirect('item_list')
    else:
        form = ImageUploadForm()
    return render(request, 'magazyn/additem.html', {'form': form})


def item_inventory_count(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    count = Inventory.objects.filter(gtin=item.gtin).count()
    return render(request, 'item_inventory.html', {
        'item': item,
        'inventory_count': count
    })

def add_inventory_item(request):
    if request.method == 'POST':
        form = AddToInventory(request.POST)
        if form.is_valid():
            form.save()
            action = request.POST.get('action')
            if action == 'save_and_to_new':
                return redirect('add_inventory_item')  # adjust name as needed
            else:
                return redirect('inventory_list')
    else:
        form = AddToInventory()
    return render(request, 'magazyn/addinventory.html', {'form': form})

