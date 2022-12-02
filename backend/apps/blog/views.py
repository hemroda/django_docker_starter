from django.views.generic import ListView

from .models import Post


class IndexBlogView(ListView):
    model = Post
    template_name = "blog/index.html"
