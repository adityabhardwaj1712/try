from rest_framework.routers import DefaultRouter
from .views import OrganizationViewSet, MembershipViewSet

router = DefaultRouter()
router.register("organizations", OrganizationViewSet, basename="organizations")
router.register("memberships", MembershipViewSet, basename="memberships")

urlpatterns = router.urls