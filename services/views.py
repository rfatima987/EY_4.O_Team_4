from django.shortcuts import render, redirect
from .models import ServiceProvider

def home(request):
    return render(request, 'index.html')

def providers(request):
    data = ServiceProvider.objects.all()
    return render(request, 'providers.html', {'providers': data})

def add_provider(request):
    if request.method == "POST":
        ServiceProvider.objects.create(
            name=request.POST['name'],
            profession=request.POST['profession'],
            phone=request.POST['phone'],
            location=request.POST['location']
        )
        return redirect('providers')
    return render(request, 'provider_register.html')