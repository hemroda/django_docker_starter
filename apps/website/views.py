from django.shortcuts import render

from datetime import datetime


def homepage(request):
    return render(request, "website/homepage.html",
                  context={
                      "date": datetime.today()
                  }
                )
