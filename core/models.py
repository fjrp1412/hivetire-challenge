from django.db import models
from .enums import VehicleInspectionStatus


class Vehicle(models.Model):
    active = models.BooleanField()
    plate = models.CharField(max_length=200)
    brand = models.CharField(max_length=200)
    type = models.CharField(max_length=200)
    fleet = models.CharField(max_length=200)

    def get_last_inspection(self) -> "VehicleInspection | None":
        return self.vehicleinspection_set.order_by("-date").first()


    def get_in_progress_inspection(self) -> "VehicleInspection | None":
        return self.vehicleinspection_set.filter(
            status=VehicleInspectionStatus.IN_PROGRESS
        ).first()

# We could add a db validation with (pk, status) for only one inspection to be in progress
class VehicleInspection(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    # we could split date as created_at and inspected_at to avoid confusion. For now, we assume this is the created at date
    date = models.DateTimeField()
    odometer = models.FloatField(default=0)
    status = models.IntegerField(choices=VehicleInspectionStatus.choices)


    def mark_as_completed(self):
        self.status = VehicleInspectionStatus.COMPLETED
        self.save(update_fields=["status"])

    @property
    def is_in_progress(self) -> bool:
        return self.status == VehicleInspectionStatus.IN_PROGRESS
