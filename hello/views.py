import os
from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from numpy.ma.core import less_equal

from hello.models import Task
from hello.models import Inventory
from hello.models import Item

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
    inventories = Inventory.objects.all()
    context = {
        "title": "Inventory List",
        "inventories": inventories
    }
    return render(request, "magazyn/inventory_list.html", context=context)

def product_details_view(request,pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    context={
        'inventory': inventory
    }
    return render(request, "magazyn/product_details.html", context= context)

def item_list(request):
    sort_by = request.GET.get('sort_by', 'name')  # Default to sorting by 'name':
    sort_dir = request.GET.get('sort_direction', 'asc')  # Default to direction ascending
    if sort_dir=="asc":
        items = Item.objects.all().order_by(sort_by)
    if sort_dir=="desc":
        items = Item.objects.all().order_by("-"+sort_by)
    return render(request, 'magazyn/item_list.html', {'items': items, 'sort_by': sort_by})

def update_item_order(request):
    if request.method == 'POST':
        # Assuming the order is sent as a list of item IDs in the request
        item_order = request.POST.getlist('item_order[]')

        # Update the order of items in the database (you may need to add an order field)
        for index, item_id in enumerate(item_order):
            item = Item.objects.get(id=item_id)
            item.order = index  # Assuming an 'order' field exists in your model
            item.save()

        return JsonResponse({'status': 'success'})