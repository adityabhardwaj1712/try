from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Organization, Membership


@login_required
def organization_list(request):

    organizations = Organization.objects.filter(
        memberships__user=request.user
    ).distinct()

    return render(
        request,
        "dashboard/organization_list.html",
        {"organizations": organizations}
    )


@login_required
def create_organization(request):

    if not request.user.can_manage():
        return HttpResponseForbidden("Permission denied")

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

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

    return render(request, "dashboard/create_organization.html")


@login_required
def organization_detail(request, pk):

    organization = get_object_or_404(Organization, id=pk)

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