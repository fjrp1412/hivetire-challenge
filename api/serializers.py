from rest_framework.serializers import ModelSerializer

from core.models import Vehicle
from core.models import VehicleInspection


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleInspectionSerializer(ModelSerializer):
    class Meta:
        model = VehicleInspection
        fields = "__all__"
