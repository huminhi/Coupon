from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.
# this login required decorator is to not allow to any
# view without authenticating
class Authentication():

    def login(self, request):
        return render(request,"home.html")

    def logout(self, request):
        pass