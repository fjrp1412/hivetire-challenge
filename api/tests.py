from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from core.enums import VehicleInspectionStatus
from core.models import Vehicle, VehicleInspection


def make_vehicle(**kwargs) -> Vehicle:
    defaults = {"active": True, "plate": "ABC-123", "brand": "Toyota", "type": "Camión", "fleet": "Norte"}
    defaults.update(kwargs)
    return Vehicle.objects.create(**defaults)


def make_inspection(vehicle: Vehicle, insp_status=VehicleInspectionStatus.IN_PROGRESS, **kwargs) -> VehicleInspection:
    defaults = {"vehicle": vehicle, "status": insp_status, "date": timezone.now(), "odometer": 1000}
    defaults.update(kwargs)
    return VehicleInspection.objects.create(**defaults)


class CreateInspectionTest(APITestCase):
    def setUp(self):
        self.url = reverse("api:inspection-list")
        self.vehicle = make_vehicle()

    def test_creates_inspection_and_returns_full_data(self):
        response = self.client.post(self.url, {"vehicle_id": self.vehicle.pk, "odometer_km": 5000})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["status"], VehicleInspectionStatus.IN_PROGRESS)
        self.assertEqual(response.data["vehicle_id"], self.vehicle.pk)
        self.assertIn("id", response.data)
        self.assertIn("date", response.data)

    def test_vehicle_not_active_returns_400(self):
        vehicle = make_vehicle(active=False, plate="XYZ-999")
        response = self.client.post(self.url, {"vehicle_id": vehicle.pk, "odometer_km": 5000})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vehicle_not_found_returns_400(self):
        response = self.client.post(self.url, {"vehicle_id": 99999, "odometer_km": 5000})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_vehicle_already_has_inspection_in_progress_returns_409(self):
        make_inspection(self.vehicle)
        response = self.client.post(self.url, {"vehicle_id": self.vehicle.pk, "odometer_km": 6000})

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_completed_vehicle_inspection_allows_new_one(self):
        make_inspection(self.vehicle, insp_status=VehicleInspectionStatus.COMPLETED)
        response = self.client.post(self.url, {"vehicle_id": self.vehicle.pk, "odometer_km": 6000})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class FinalizeInspectionTest(APITestCase):
    def setUp(self):
        self.vehicle = make_vehicle()

    def _url(self, pk: int) -> str:
        return reverse("api:inspection-finalize", kwargs={"pk": pk})

    def test_finalizes_inspection_successfully(self):
        inspection = make_inspection(self.vehicle)
        response = self.client.patch(self._url(inspection.pk))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], VehicleInspectionStatus.COMPLETED)
        inspection.refresh_from_db()
        self.assertEqual(inspection.status, VehicleInspectionStatus.COMPLETED)

    def test_already_completed_returns_409(self):
        inspection = make_inspection(self.vehicle, insp_status=VehicleInspectionStatus.COMPLETED)
        response = self.client.patch(self._url(inspection.pk))

        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def test_inspection_not_found_returns_404(self):
        response = self.client.patch(self._url(99999))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
