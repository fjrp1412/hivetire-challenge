from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from core.models import Vehicle
from core.models import VehicleInspection


class VehicleSerializer(ModelSerializer):
    class Meta:
        model = Vehicle
        fields = "__all__"


class VehicleInspectionSerializer(ModelSerializer):
    vehicle_id = serializers.IntegerField(source="vehicle.id")
    vehicle_plate = serializers.CharField(source="vehicle.plate")

    class Meta:
        model = VehicleInspection
        # we should manage odometer as odometer_km in the API for consistency
        fields = ["id", "status", "date", "odometer", "vehicle_id", "vehicle_plate"]


class InspectionShortSerializer(ModelSerializer):
    status = SerializerMethodField()
    odometer_km = serializers.FloatField(source="odometer")

    def get_status(self, obj: VehicleInspection) -> str:
        return obj.get_status_display()

    class Meta:
        model = VehicleInspection
        fields = ["date", "odometer_km", "status"]
        extra_kwargs = {
            "date": {"format": "%Y-%m-%d"},
        }


class VehicleDetailSerializer(VehicleSerializer):
    last_inspection = SerializerMethodField()

    def get_last_inspection(self, obj: Vehicle) -> dict | None:
        inspection = obj.get_last_inspection()
        if inspection is None:
            return None
        return InspectionShortSerializer(inspection).data

    class Meta(VehicleSerializer.Meta):
        pass

class VehicleInspectionCreateSerializer(ModelSerializer):
    vehicle_id = serializers.PrimaryKeyRelatedField(
        queryset=Vehicle.objects.all(), source="vehicle",
        error_messages={"does_not_exist": "El vehículo con id '{pk_value}' no existe."}
    )
    odometer_km = serializers.FloatField(source="odometer", min_value=0)

    class Meta:
        model = VehicleInspection
        fields = ["vehicle_id", "odometer_km"]

