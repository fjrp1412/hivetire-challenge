from django.utils import timezone
from rest_framework.exceptions import ValidationError

from core.models import Vehicle, VehicleInspection
from core.enums import VehicleInspectionStatus


class InspectionConflictError(Exception):
    pass


class InspectionService:
    @staticmethod
    def create_inspection(vehicle: Vehicle, odometer: float) -> VehicleInspection:
        if not vehicle.active:
            raise ValidationError({"vehicle_id": "El vehículo no está activo."})
        if in_progress_inspection := vehicle.get_in_progress_inspection():
            raise InspectionConflictError(
                "El vehículo ya tiene una inspección en curso. "
                f"ID de la inspeccion en curso: {in_progress_inspection.id}"
            )
        return VehicleInspection.objects.create(
            vehicle=vehicle,
            odometer=odometer,
            status=VehicleInspectionStatus.IN_PROGRESS,
            date=timezone.now(),
        )

    @staticmethod
    def finalize_inspection(inspection: VehicleInspection) -> VehicleInspection:
        if not inspection.is_in_progress:
            raise InspectionConflictError("La inspección no está en curso.")
        inspection.mark_as_completed()
        return inspection
