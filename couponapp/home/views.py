from django.http import HttpResponse

class HomeView():
    def __int__(self):
        pass

    def index(self, request):
        return HttpResponse('template/index.')