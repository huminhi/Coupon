from  django.views.generic.base import TemplateResponseMixin, TemplateView

from couponapp import models


class HomeView(TemplateView):
    template_name = "index.html"
    def __int__(self, request):
        return self.index(request)

    def index(self, request):
        temp = models.CappCouponCodes.objects.all()
        return TemplateResponseMixin.render_to_response()