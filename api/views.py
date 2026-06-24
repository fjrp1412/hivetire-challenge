from rest_framework.viewsets import ModelViewSet
from core.models import Vehicle
from core.models import VehicleInspection
from api.serializers import VehicleDetailSerializer, VehicleInspectionSerializer
from api.serializers import VehicleSerializer


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return VehicleDetailSerializer
            case _:
                return super().get_serializer_class()

class VehicleInspectionViewSet(ModelViewSet):
    queryset = VehicleInspection.objects.all()
    serializer_class = VehicleInspectionSerializer