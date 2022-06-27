from django.shortcuts import render
from scripts.models import Object
from scripts.sql import query
from math import ceil

DATABASE = "data/piratebay.db"
TABLE = "courses"


def list2pages(data:list, size:int) -> dict:

    # calculate the batch
    max_page = ceil(len(data)/size)
    pages = [i*size for i in range(max_page+1)]
    pages[-1] = len(data)

    # assign the data in pages into the containers
    containers = {}
    for i in range(max_page):
        a,b = pages[i],pages[i+1]
        containers.update({i+1:data[a:b]})
    
    # return the value
    return containers

def configure_pagination(models:dict, active:int):
    page_len = 10
    n = len(models)
    all_pages = [page_len*(i+1) for i in range(ceil(n/page_len))]
    all_pages[-1] = n

    start = next((i-page_len+1 for i in all_pages if active <= i),1)
    end = next((i for i in all_pages if active <= i),10)

    if n-active < page_len:
        start = n-page_len+1
        end = n

    pagination = [i for i in range(start,end+1)]
    return pagination

# request route
def root(request):

    # query the database
    cmd = f"SELECT * FROM {TABLE};"
    data = query(cmd,DATABASE)
    contents = Object(data)

    # sort data by dates by default
    sort_value = request.GET.get('sort_by','uploaded')
    contents.sort_by(sort_value)

    # turn models into pages data
    size = 15
    models = list2pages(contents.models,size)

    # find pagination length
    page = request.GET.get('page',1)
    page = int(page)
    paginations = configure_pagination(models,page)

    # define the context
    context=dict(
        models=models.get(page),
        paginations=paginations,
        max_page=len(paginations),
        active_page=page,
        total_contents=len(models.get(page)),
        prev_page=min(paginations),
        next_page=max(paginations),
        rows=size
    )
    return render(request,"index.html",context)

def search(request):
    context={}
    return render(request,"index.html",context)