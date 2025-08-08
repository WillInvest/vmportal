from django.contrib import admin
from django.core.mail import send_mail
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("last_name","first_name","email","status","vm_id","created_at")
    list_filter = ("status","course","created_at")
    search_fields = ("first_name","last_name","email","vm_id")
    actions = ["approve_and_notify","mark_vm_assigned_and_notify"]

    @admin.action(description="Approve selected (and email student)")
    def approve_and_notify(self, request, qs):
        n=0
        for app in qs:
            app.status = Application.Status.APPROVED
            app.save()
            send_mail(
                "Your VM request was approved",
                f"Hi {app.first_name}, your request was approved.\n"
                f"Check status: {request.build_absolute_uri(f'/status/{app.status_token}/')}",
                None, [app.email], fail_silently=True
            )
            n+=1
        self.message_user(request, f"Approved + emailed {n} application(s).")

    @admin.action(description="Mark VM assigned (and email details)")
    def mark_vm_assigned_and_notify(self, request, qs):
        n=0
        for app in qs:
            app.status = Application.Status.VM_ASSIGNED
            app.save()
            send_mail(
                "Your VM is ready",
                f"Hi {app.first_name}, your VM is ready.\n"
                f"VM ID: {app.vm_id}\nNotes: {app.staff_notes}\n"
                f"Status: {request.build_absolute_uri(f'/status/{app.status_token}/')}",
                None, [app.email], fail_silently=True
            )
            n+=1
        self.message_user(request, f"Marked VM_ASSIGNED + emailed {n} application(s).")
