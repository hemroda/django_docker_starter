from datetime import date

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods
from oauth2_provider.models import Application

from .forms import CustomAuthenticationForm, CustomUserCreationForm


@login_required
def profile(request):
    try:
        return render(
            request,
            "accounts/profile.html",
            {
                "today": date.today(),
            },
        )
    except Exception:
        return redirect("login")


def register_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Automatically create an OAuth application for the user
            Application.objects.create(
                user=user,
                client_type=Application.CLIENT_CONFIDENTIAL,
                authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
                name=f"{user.username}'s Application",
            )

            # Authenticate the user with ModelBackend
            authenticated_user = authenticate(
                request,
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password1"],
                backend="django.contrib.auth.backends.ModelBackend",
                # Explicitly specify the backend to use for registration
            )

            if authenticated_user is not None:
                login(
                    request,
                    authenticated_user,
                    backend="django.contrib.auth.backends.ModelBackend",
                )
                messages.success(request, "Registration successful.")
                next_url = request.GET.get("next", "accounts_profile_path")
                return redirect(next_url)
            else:
                messages.error(
                    request, "Error during authentication after registration."
                )
    else:
        form = CustomUserCreationForm()
    return render(request, "accounts/authentication/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("website_homepage_path")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")

    form = CustomAuthenticationForm()
    return render(request, "accounts/authentication/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("website_homepage_path")


@login_required
def get_oauth_token(request):
    """
    Generate or retrieve OAuth token for the current user
    """
    # Find the user's OAuth application
    try:
        app = Application.objects.get(user=request.user)
    except Application.DoesNotExist:
        app = Application.objects.create(
            user=request.user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_CLIENT_CREDENTIALS,
            name=f"{request.user.username}'s Application",
        )

    # Generate or retrieve access token
    from datetime import timedelta

    from django.utils import timezone
    from oauth2_provider.models import AccessToken

    # Check for existing valid token
    existing_token = AccessToken.objects.filter(
        user=request.user, expires__gt=timezone.now()
    ).first()

    if existing_token:
        return render(
            request,
            "accounts/authentication/token.html",
            {"token": existing_token.token, "expires": existing_token.expires},
        )

    # Create or retrieve existing token
    token = AccessToken.objects.create(
        user=request.user,
        token="".join(secrets.token_urlsafe(32)),
        application=app,
        expires=timezone.now() + timedelta(hours=10),
        scope="read write",
    )

    return render(
        request,
        "accounts/authentication/token.html",
        {"token": token.token, "expires": token.expires},
    )


# What django-app returns to your api
@require_http_methods(["GET"])
def validate_token(request):
    if request.user.is_authenticated:
        return JsonResponse(
            {
                "id": request.user.id,
                "username": request.user.username,
                "email": request.user.email,
                "is_active": request.user.is_active,
                # Add any other user details you want to return
            }
        )
    else:
        return JsonResponse({"error": "Not authenticated"}, status=401)
