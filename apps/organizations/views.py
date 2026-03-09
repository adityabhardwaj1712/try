from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Organization, Membership

@login_required
def organization_list(request):

    if request.method == "POST":

        if request.user.role != "ADMIN" and not request.user.is_superuser:
            return render(
                request,
                "dashboard/no_permission.html"
            )

        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:

            org = Organization.objects.create(
                name=name,
                description=description,
                owner=request.user
            )

            Membership.objects.create(
                user=request.user,
                organization=org,
                role="ADMIN"
            )

            return redirect("/organizations/")

    organizations = Organization.objects.filter(
        memberships__user=request.user
    ).distinct()

    return render(
        request,
        "dashboard/organization_list.html",
        {
            "organizations": organizations
        }
    )


@login_required
def create_organization(request):

    if request.method == "POST":

        if request.user.role != "ADMIN" and not request.user.is_superuser:
            return render(
                request,
                "dashboard/no_permission.html"
            )

        name = request.POST.get("name")
        description = request.POST.get("description")

        if not name:
            return render(
                request,
                "dashboard/create_organization.html",
                {
                    "error": "Organization name is required"
                }
            )

        org = Organization.objects.create(
            name=name,
            description=description,
            owner=request.user
        )

        Membership.objects.create(
            user=request.user,
            organization=org,
            role="ADMIN"
        )

        return redirect("organization_list")

    return render(
        request,
        "dashboard/create_organization.html"
    )


@login_required
def organization_detail(request, pk):

    organization = get_object_or_404(
        Organization,
        id=pk
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

    members = Membership.objects.filter(
        organization=organization
    ).select_related("user")

    return render(
        request,
        "dashboard/organization_detail.html",
        {
            "organization": organization,
            "members": members
        }
    )