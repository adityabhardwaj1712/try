from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden

from .models import Organization, Membership


# ===============================
# ORGANIZATION LIST
# ===============================


@login_required
def organization_list(request):

    # allow only admin or manager
    if request.user.role not in ["ADMIN", "MANAGER"] and not request.user.is_superuser:
        return HttpResponseForbidden("Permission denied")

    # CREATE ORGANIZATION
    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        if name:

            org = Organization.objects.create(
                name=name,
                description=description,
                owner=request.user
            )

            # create membership
            Membership.objects.create(
                user=request.user,
                organization=org,
                role="ADMIN"
            )

            return redirect("/organizations/")

    # SHOW ORGANIZATIONS
    organizations = Organization.objects.all()

    return render(
        request,
        "dashboard/organization_list.html",
        {
            "organizations": organizations
        }
    )

# ===============================
# CREATE ORGANIZATION
# ===============================
@login_required
def create_organization(request):

    print("CREATE ORG VIEW CALLED")

    if request.method == "POST":

        name = request.POST.get("name")
        description = request.POST.get("description")

        print("DATA RECEIVED:", name, description)

        org = Organization.objects.create(
            name=name,
            description=description,
            owner=request.user
        )

        print("ORG CREATED:", org.id)

        Membership.objects.create(
            user=request.user,
            organization=org,
            role="ADMIN"
        )

        return redirect("organization_list")

    return render(request, "dashboard/create_organization.html")


# ===============================
# ORGANIZATION DETAIL
# ===============================

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