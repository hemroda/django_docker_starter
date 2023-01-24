from .forms import CustomUserCreationForm
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView


class SignUpView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/signup.html"


class DashboardView(TemplateView):
    template_name = "accounts/dashboard.html"
