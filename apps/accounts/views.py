from django.shortcuts import render

from datetime import datetime


def dashboard(request):
    return render(request, "accounts/dashboard.html",
                  context={
                      "date": datetime.today()
                  }
                )
