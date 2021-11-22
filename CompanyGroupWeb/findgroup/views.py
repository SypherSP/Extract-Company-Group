from django.shortcuts import redirect, render
from django.http import response,HttpResponseRedirect
from django.urls import reverse
from . import generateFile 

# Create your views here.

def index(request):
    if request.method == "POST":
        print("-------------------")
        print(request.POST['URL'])
        generateFile.execute(request.POST['URL'])
        return HttpResponseRedirect(reverse("findgroup:index"))
        
    return render(request, 'findgroup/index.html')