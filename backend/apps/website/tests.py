from django.test import SimpleTestCase
from django.urls import reverse


class HomepageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
    
    def test_url_available_by_name(self):
        response = self.client.get(reverse("website_homepage_path"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("website_homepage_path"))
        self.assertTemplateUsed(response, "website/home.html")

    def test_template_content(self):
        response = self.client.get(reverse("website_homepage_path"))
        self.assertContains(response, "<h1>Django Docker Starter</h1>")


class AboutpageTests(SimpleTestCase):
    def test_url_exists_at_correct_location(self):
        response = self.client.get("/about")
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):
        response = self.client.get(reverse("website_about_path"))
        self.assertEqual(response.status_code, 200)

    def test_template_name_correct(self):
        response = self.client.get(reverse("website_about_path"))
        self.assertTemplateUsed(response, "website/about.html")

    def test_template_content(self):
        response = self.client.get(reverse("website_about_path"))
        self.assertContains(response, "<h1>About us</h1>") 