from django.urls import path
from .views import SignUpView, DashboardView

urlpatterns = [
    path("signup/", SignUpView.as_view(), name="accounts_signup_path"),
    path("dashboard/", DashboardView.as_view(), name="accounts_dashboard_path"),
]
