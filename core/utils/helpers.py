def get_fields(serializer):
    """Obtains a serializer's fields and returns them as a list.

    Args:
        serializer (ModelSerializer): A Django serializer class (inherits from ModelSerializer).

    Returns:
        A list of fields as strings.
    """

    fields = []

    for key in serializer().fields:
        fields.append(key)

    return fields
