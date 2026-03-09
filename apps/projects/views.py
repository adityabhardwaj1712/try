from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from apps.organizations.models import Organization, Membership
from .models import Project

@login_required
def project_list(request):

    projects = Project.objects.filter(
        organization__memberships__user=request.user
    ).select_related(
        "organization",
        "owner"
    ).distinct().order_by("-id")

    organizations = Organization.objects.filter(
        memberships__user=request.user
    ).order_by("name")

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

    organizations = Organization.objects.filter(
        memberships__user=request.user
    ).order_by("name")

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")
        organization_id = request.POST.get("organization")

        if not name:
            return render(
                request,
                "dashboard/create_project.html",
                {
                    "organizations": organizations,
                    "error": "Project name is required."
                }
            )

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

        membership = Membership.objects.filter(
            user=request.user,
            organization=organization
        ).first()

        if not membership:
            return render(
                request,
                "dashboard/no_permission.html"
            )

        if membership.role == "VIEWER":
            return render(
                request,
                "dashboard/no_permission.html"
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

    membership = Membership.objects.filter(
        user=request.user,
        organization=project.organization
    ).first()

    if not membership:
        return render(
            request,
            "dashboard/no_permission.html"
        )

    return render(
        request,
        "dashboard/project_detail.html",
        {
            "project": project
        }
    )