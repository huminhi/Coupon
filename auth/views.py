from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# this login required decorator is to not allow to any  
# view without authenticating
@login_required(login_url="login/")
def login(request):
    return render(request, "index.html")

@login_required(login_url="logout/")
def logout(request):
    return render(request, "index.html")