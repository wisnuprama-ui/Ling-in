from django.shortcuts import render

response ={}
# Create your views here.
def index(request):
    return render(request, 'layout/base.html', response)