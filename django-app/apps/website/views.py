from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "website/homepage.html"


class AboutPageView(TemplateView):
    template_name = "website/about.html"
