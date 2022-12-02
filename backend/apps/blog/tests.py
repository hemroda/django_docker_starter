from django.test import TestCase
from django.urls import reverse

from apps.blog.models import Post


class PostTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.post = Post.objects.create(
                    body="Sed ut perspiciatis unde omnis iste natus error sit voluptatem accusantium doloremque.",
                    title="Lorem title",
                    author="JSmith")

    def test_model_content(self):
        self.assertEqual(self.post.title, "Lorem title")
        self.assertEqual(self.post.author, "JSmith")
 
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/blog")
        self.assertEqual(response.status_code, 200)
    
    def test_index_page(self):
        response = self.client.get(reverse("blog_index_path"))
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, "blog/index.html") 
        self.assertContains(response, "JSmith")