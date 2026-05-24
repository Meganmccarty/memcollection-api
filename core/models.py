from django.db import models


class TimeStampMixin(models.Model):
    """This is an abstract class for managing when a model instance is created and when it is
    modified.

    Attributes:
        date_created (str): The date the model was created.
        date_modified (str): The date the model was modified.
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
