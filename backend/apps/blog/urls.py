from django.urls import path
from .views import IndexBlogView

urlpatterns = [
    path("", IndexBlogView.as_view(), name="blog_index_path"),
]