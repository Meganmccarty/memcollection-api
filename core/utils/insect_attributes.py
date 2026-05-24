from django.db.models import TextChoices


class Sex(TextChoices):
    MALE = "male", "male"
    FEMALE = "female", "female"
    UNKNOWN = "unknown", "unknown"


class Stage(TextChoices):
    EGG = "egg", "egg"
    LARVA = "larva", "larva"
    NYMPH = "nymph", "nymph"
    PUPA = "pupa", "pupa"
    ADULT = "adult", "adult"
