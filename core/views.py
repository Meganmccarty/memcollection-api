from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.db.models import RestrictedError
from django.http import HttpResponseRedirect
from django.urls import NoReverseMatch, reverse
from django.utils.html import format_html, mark_safe
from wagtail.admin.views.generic import DeleteView
from wagtail.snippets.views.snippets import SnippetViewSet


class CustomSnippetDeleteView(DeleteView):
    def form_valid(self, form):
        """Overrides the default form_valid method so that RestrictedErrors can be handled. These \
        errors occur when on_delete is set to RESTRICT and the object that we're trying to delete \
        is referenced by another object (it's foreign key is protected). Rather than show a 500 \
        Internal Server Error (when debug = False) or a stack trace (when debug = True), we catch \
        the error, stay on the page, and display it in a warning banner.

            Raises:
                PermissionDenied: If the object being deleted has a usage that is protected.
            
            Returns:
                HttpResponseRedirect: If RestrictedError is found, stay on page. If deletion is \
                successful, redirect to success_url.
        """

        if self.usage and self.usage.is_protected:
            raise PermissionDenied
        try:
            super().delete_action()
        except RestrictedError as e:
            return self._handle_restricted_error(e)
        success_url = self.get_success_url()
        messages.success(self.request, self.get_success_message())
        hook_response = self.run_after_hook()
        if hook_response is not None:
            return hook_response
        return HttpResponseRedirect(success_url)


    def _handle_restricted_error(self, error: RestrictedError):
        """Handles RestrictedError exceptions raised when trying to delete an object that is \
        referenced by another object with a protected foreign key. Displays an error message \
        in Wagtail's warning banner, with each protected object linked to that object's edit \
        view in Wagtail).
    
            Returns:
                HttpResponseRedirect: Redirects to the same page, with an error message in the \
                banner.
        """

        by_model = {}
        for obj in error.restricted_objects:
            by_model.setdefault(obj.__class__, []).append(obj)

        parts = []

        for model_class, objs in by_model.items():
            model_name = model_class._meta.verbose_name_plural.title()
            links = []
            for obj in objs:
                try:
                    edit_url = reverse(
                        f"wagtailsnippets_{model_class._meta.app_label}_{model_class._meta.model_name}:edit", args=[obj.pk],
                    )
                    links.append(format_html('<a href="{}">{}</a>', edit_url, str(obj)))
                except NoReverseMatch:
                    links.append(format_html('{}', str(obj)))
            parts.append(format_html("{}: {}", model_name, mark_safe(", ".join(links))))

        detail = "; ".join(parts)

        messages.error(
            self.request,
            mark_safe(f"Cannot delete — model instance referenced by: {detail}")
        )

        from django.shortcuts import redirect
        return redirect(self.get_delete_url())


class SnippetWithCustomDeleteViewSet(SnippetViewSet):
    """A SnippetViewSet that uses the CustomSnippetDeleteView for handling RestrictedErrors."""

    delete_view_class = CustomSnippetDeleteView