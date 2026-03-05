from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from apps.organizations.models import Organization
from .models import Project


@login_required
def project_list(request):

    projects = Project.objects.select_related(
        "organization",
        "owner"
    ).all()

    organizations = Organization.objects.all()

    return render(
        request,
        "dashboard/project_list.html",
        {
            "projects": projects,
            "organizations": organizations
        }
    )


@login_required
def create_project(request):

    organizations = Organization.objects.all()

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        organization_id = request.POST.get("organization")

        if not organization_id:

            return render(
                request,
                "dashboard/create_project.html",
                {
                    "organizations": organizations,
                    "error": "Please select an organization."
                }
            )

        organization = get_object_or_404(
            Organization,
            id=organization_id
        )

        Project.objects.create(
            name=name,
            description=description,
            organization=organization,
            owner=request.user
        )

        return redirect("project_list")

    return render(
        request,
        "dashboard/create_project.html",
        {
            "organizations": organizations
        }
    )


@login_required
def project_detail(request, pk):

    project = get_object_or_404(
        Project.objects.select_related(
            "organization",
            "owner"
        ),
        id=pk
    )

    return render(
        request,
        "dashboard/project_detail.html",
        {
            "project": project
        }
    )