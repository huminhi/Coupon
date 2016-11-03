__author__ = 'Hieu Huynh'
from django.views.generic.base import TemplateResponseMixin, TemplateView, TemplateResponse
from couponapp import models
from django.conf import settings

class HomeView(TemplateView):

    def get_context_data(self, request=None, **kwargs):
        qs = models.CappCouponCodes.objects.all()
        coupons = []
        for item in qs:
            coupons.append(item)
        context = {'coupons': coupons}
        return context

    def index(self, request):
        return TemplateView.render_to_response()

    def get(self, request):
        context = self.get_context_data(request)
        return TemplateResponse(request, template="index.html", context=context)