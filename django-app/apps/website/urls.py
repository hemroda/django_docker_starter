from django.urls import path

from .views import AboutPageView, HomePageView

urlpatterns = [
    path("", HomePageView.as_view(), name="website_homepage_path"),
    path("about/", AboutPageView.as_view(), name="website_about_path"),
]
