from django.db.models import IntegerChoices

class VehicleInspectionStatus(IntegerChoices):
    IN_PROGRESS = (1, "En Curso")
    COMPLETED = (2, "Finalizada")