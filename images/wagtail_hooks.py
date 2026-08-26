# myapp/wagtail_hooks.py
from django.utils.html import format_html
from django.templatetags.static import static
from wagtail import hooks


@hooks.register("insert_global_admin_js")
def global_admin_js():
    return format_html('<script src="{}"></script>', static("js/memcollection.js"))
