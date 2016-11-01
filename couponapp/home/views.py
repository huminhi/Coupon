from django.views.generic.base import TemplateResponseMixin, TemplateView
from couponapp import models


class HomeView(TemplateView):
    template_name = "index.html"
    def __int__(self, request):
        return self.index(self, request)

    def index(self, request):
        # if settings["HIDE_DOCS"]:
        #     raise Http404("Django Rest Framework Docs are hidden. Check your settings.")
        #
        # context = super(DRFDocsView, self).get_context_data(**kwargs)
        # docs = ApiDocumentation()
        # endpoints = docs.get_endpoints()
        #
        # query = self.request.GET.get("search", "")
        # if query and endpoints:
        #     endpoints = [endpoint for endpoint in endpoints if query in endpoint.path]
        #
        # context['query'] = query
        # context['endpoints'] = endpoints
        # return context
        return TemplateView.render_to_response()