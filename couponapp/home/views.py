from django.http import HttpResponse
from  django.views.generic.base import TemplateResponse, TemplateResponseMixin, TemplateView
# from django.views.generic import

class HomeView(TemplateView):
    template_name = "index.html"
    def __int__(self, request):
        return self.index(request)

    def index(self, request):
        return TemplateResponseMixin.render_to_response()