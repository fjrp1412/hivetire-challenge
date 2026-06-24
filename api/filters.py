import django_filters
from django import forms
from core.models import Vehicle, VehicleInspection
from core.enums import VehicleInspectionStatus

DATE_FORMAT = "%Y-%m-%d"
DATE_FORMAT_DISPLAY = "YYYY-MM-DD"


class DateFormField(forms.DateTimeField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("input_formats", [DATE_FORMAT])
        super().__init__(*args, **kwargs)

    def to_python(self, value):
        try:
            return super().to_python(value)
        except forms.ValidationError:
            raise forms.ValidationError(
                f"Formato de fecha invalido: '{value}'. El formato esperado es {DATE_FORMAT_DISPLAY}."
            )


class DateRangeFilter(django_filters.Filter):
    field_class = DateFormField


class VehicleFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id")
    active = django_filters.BooleanFilter(field_name="active")
    brand = django_filters.CharFilter(field_name="brand", lookup_expr="icontains")
    type = django_filters.CharFilter(field_name="type", lookup_expr="iexact")
    fleet = django_filters.CharFilter(field_name="fleet", lookup_expr="iexact")
    plate = django_filters.CharFilter(field_name="plate", lookup_expr="icontains")
    has_active_inspection = django_filters.BooleanFilter(method="filter_has_active_inspection")

    class Meta:
        model = Vehicle
        fields = ["id", "active", "brand", "type", "fleet", "plate"]

    def filter_has_active_inspection(self, queryset, name, value):
        if value is None:
            return queryset

        if value:
            return queryset.filter(
                vehicleinspection__status=VehicleInspectionStatus.IN_PROGRESS
            ).distinct()
        return queryset.exclude(
            vehicleinspection__status=VehicleInspectionStatus.IN_PROGRESS
        )


class VehicleInspectionFilter(django_filters.FilterSet):
    id = django_filters.NumberFilter(field_name="id")
    vehicle = django_filters.NumberFilter(field_name="vehicle_id")
    date_from = DateRangeFilter(field_name="date", lookup_expr="gte")
    date_to = DateRangeFilter(field_name="date", lookup_expr="lte")
    status = django_filters.ChoiceFilter(choices=VehicleInspectionStatus.choices)

    class Meta:
        model = VehicleInspection
        fields = ["id", "vehicle", "status"]
