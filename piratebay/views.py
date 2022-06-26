from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return HttpResponse("<h1>my app</h1>")

def demo(request):
    context = dict(
        name="Ekky Armandi",
        today=datetime.now()
    )
    return render(request,"demo.html",context)