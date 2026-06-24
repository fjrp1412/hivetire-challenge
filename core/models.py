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


class VehicleInspection(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE)
    date = models.DateTimeField()
    odometer = models.FloatField(default=0)
    status = models.IntegerField(choices=VehicleInspectionStatus.choices)
