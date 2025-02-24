from django.urls import path

from . import views

urlpatterns = [
    # TODO: Uncomment when the applications are open to all users
    # path('register/', views.register_view, name="accounts_register_path"),
    path("login/", views.login_view, name="accounts_login_path"),
    path("logout/", views.logout_view, name="accounts_logout_path"),
    path("profile/", views.profile, name="accounts_profile_path"),
    path("get-token/", views.get_oauth_token, name="get_token"),
    # path bellow is used in FastAPI
    path("validate-token/", views.validate_token, name="validate_token"),
]
