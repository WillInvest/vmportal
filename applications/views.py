from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from .forms import ApplicationForm
from .models import Application

def apply(request):
    if request.method == "POST":
        form = ApplicationForm(request.POST)
        if form.is_valid():
            app = form.save()
            send_mail(
                "VM request received",
                f"Thanks {app.first_name}! Check status: "
                f"{request.build_absolute_uri(f'/status/{app.status_token}/')}",
                None, [app.email], fail_silently=True
            )
            messages.success(request, "Submitted! Check your email for a status link.")
            return redirect("apply")
    else:
        form = ApplicationForm()
    return render(request, "applications/apply.html", {"form": form})

def status(request, token):
    app = get_object_or_404(Application, status_token=token)
    return render(request, "applications/status.html", {"app": app})
