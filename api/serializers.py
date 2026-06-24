from rest_framework.serializers import ModelSerializer, SerializerMethodField

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


class InspectionShortSerializer(ModelSerializer):
    status = SerializerMethodField()

    def get_status(self, obj: VehicleInspection) -> str:
        return obj.get_status_display()

    class Meta:
        model = VehicleInspection
        fields = ["date", "odometer", "status"]

class VehicleDetailSerializer(VehicleSerializer):
    last_inspection = SerializerMethodField()

    def get_last_inspection(self, obj: Vehicle) -> dict | None:
        inspection = obj.get_last_inspection()
        if inspection is None:
            return None
        return InspectionShortSerializer(inspection).data

    class Meta(VehicleSerializer.Meta):
        pass