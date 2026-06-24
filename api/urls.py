from rest_framework.routers import DefaultRouter
from api.views import VehicleViewSet
from api.views import VehicleInspectionViewSet

app_name = "api"
router = DefaultRouter(trailing_slash=True)

router.register(r"vehicles", VehicleViewSet, basename="vehicle")
router.register(
    r"vehicle-inspections", VehicleInspectionViewSet, basename="vehicle-inspection"
)


urlpatterns = router.urls
