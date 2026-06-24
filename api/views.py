from rest_framework.viewsets import ModelViewSet
from core.models import Vehicle
from core.models import VehicleInspection
from api.serializers import VehicleInspectionSerializer
from api.serializers import VehicleSerializer


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

class VehicleInspectionViewSet(ModelViewSet):
    queryset = VehicleInspection.objects.all()
    serializer_class = VehicleInspectionSerializer