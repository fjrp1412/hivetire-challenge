from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Vehicle
from core.models import VehicleInspection
from api.serializers import VehicleDetailSerializer, VehicleInspectionSerializer
from api.serializers import VehicleSerializer
from api.serializers import VehicleInspectionCreateSerializer
from api.filters import VehicleFilter, VehicleInspectionFilter
from api.services import InspectionConflictError
from api.services import InspectionService


class VehicleViewSet(ModelViewSet):
    queryset = Vehicle.objects.prefetch_related("vehicleinspection_set")
    serializer_class = VehicleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VehicleFilter
    ordering_fields = ["id", "plate", "brand", "fleet", "type", "active"]
    ordering = ["plate"]

    def get_serializer_class(self):
        match self.action:
            case "retrieve":
                return VehicleDetailSerializer
            case _:
                return super().get_serializer_class()


class VehicleInspectionViewSet(ModelViewSet):
    queryset = VehicleInspection.objects.select_related("vehicle")
    serializer_class = VehicleInspectionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_class = VehicleInspectionFilter
    ordering_fields = ["id", "date", "odometer", "status"]
    ordering = ["-date"]

    def get_serializer_class(self):
        match self.action:
            case "create":
                return VehicleInspectionCreateSerializer
            case _:
                return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        vehicle = serializer.validated_data["vehicle"]
        odometer = serializer.validated_data["odometer"]

        try:
            inspection = InspectionService.create_inspection(vehicle, odometer)
        except InspectionConflictError as e:
            return Response({"vehicle_id": str(e)}, status=status.HTTP_409_CONFLICT)

        return Response(
            VehicleInspectionSerializer(inspection).data,
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=["patch"], url_path="finalize")
    def finalize(self, request, pk=None):
        inspection = self.get_object()

        try:
            InspectionService.finalize_inspection(inspection)
        except InspectionConflictError as e:
            return Response({"detail": str(e)}, status=status.HTTP_409_CONFLICT)

        return Response(VehicleInspectionSerializer(inspection).data)
