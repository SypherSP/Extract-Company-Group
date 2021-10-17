from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from scripts import generateFile 

# Create your views here.

def index(request):
    if request.method == "POST":
        print("-------------------")
        print(request.POST['URL'])
        print("-------------------")
        
    return render(request, 'findgroup/index.html')