from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def dashboard(request):
    # Add context variables here if needed
    context = {}
    return render(request, 'admin_dashboard/dashboard.html', context)
    