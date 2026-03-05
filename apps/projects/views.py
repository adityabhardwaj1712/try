from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Project
from apps.organizations.models import Organization
from apps.common.permissions import is_admin_or_manager, is_admin


@login_required
def project_list(request):

    projects = Project.objects.filter(
        members=request.user
    ).select_related("organization")

    return render(
        request,
        "dashboard/project_list.html",
        {"projects": projects}
    )


@login_required
def create_project(request, org_id):

    if not is_admin_or_manager(request.user):
        return HttpResponseForbidden("Permission denied")

    organization = get_object_or_404(Organization, id=org_id)

    if request.method == "POST":

        Project.objects.create(
            name=request.POST.get("name"),
            description=request.POST.get("description"),
            organization=organization,
            owner=request.user
        )

        return redirect("/projects/")

    return render(request, "dashboard/create_project.html")


@login_required
def delete_project(request, pk):

    project = get_object_or_404(Project, id=pk)

    if not is_admin(request.user):
        return HttpResponseForbidden("Only admin can delete")

    project.delete()

    return redirect("/projects/")