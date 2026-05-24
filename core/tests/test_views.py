from unittest.mock import MagicMock, patch
from django.test import TestCase, RequestFactory
from django.db.models import RestrictedError
from django.core.exceptions import PermissionDenied
from django.contrib.messages import get_messages
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.urls import NoReverseMatch

from core.views import CustomSnippetDeleteView


def add_middleware(request):
    """Attach session and message middleware to a request."""
    middleware = SessionMiddleware(lambda req: None)
    middleware.process_request(request)
    request.session.save()
    middleware = MessageMiddleware(lambda req: None)
    middleware.process_request(request)
    return request


class TestCustomSnippetDeleteViewFormValid(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.view = CustomSnippetDeleteView()
        self.view.object = MagicMock()
        self.view.object.pk = 1
        self.view.kwargs = {}

        self.request = add_middleware(self.factory.post("/fake-delete/"))
        self.view.request = self.request

        self.view.get_success_url = MagicMock(return_value="/success/")
        self.view.get_success_message = MagicMock(return_value="Deleted successfully.")
        self.view.get_delete_url = MagicMock(return_value="/delete/")
        self.view.usage = None

        self.restricted_obj = self._make_restricted_obj(
            "related items", "core", "relatedmodel", pk=99
        )

    def _get_messages(self):
        return [str(m) for m in get_messages(self.request)]

    def _make_restricted_obj(self, verbose_name_plural, app_label, model_name, pk=1):
        obj = MagicMock(spec=["pk", "__str__", "__class__"])
        obj.__str__ = MagicMock(return_value=f"{model_name} object ({pk})")
        obj.pk = pk
        meta = MagicMock()
        meta.verbose_name_plural = verbose_name_plural
        meta.app_label = app_label
        meta.model_name = model_name
        # Use a real type so __class__._meta works without MagicMock conflict
        obj.__class__ = type(model_name, (), {"_meta": meta})
        return obj

    def test_raises_permission_denied_when_usage_is_protected(self):
        self.view.usage = MagicMock()
        self.view.usage.is_protected = True
        with self.assertRaises(PermissionDenied):
            self.view.form_valid(MagicMock())

    def test_successful_delete_redirects_to_success_url(self):
        self.view.run_after_hook = MagicMock(return_value=None)

        with patch.object(CustomSnippetDeleteView, "delete_action"):
            response = self.view.form_valid(MagicMock())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/success/")

    def test_successful_delete_shows_success_message(self):
        self.view.run_after_hook = MagicMock(return_value=None)

        with patch.object(CustomSnippetDeleteView, "delete_action"):
            self.view.form_valid(MagicMock())

        self.assertIn("Deleted successfully.", self._get_messages())

    def test_hook_response_returned_when_not_none(self):
        hook_response = MagicMock()
        self.view.run_after_hook = MagicMock(return_value=hook_response)

        with patch.object(CustomSnippetDeleteView, "delete_action"):
            response = self.view.form_valid(MagicMock())

        self.assertEqual(response, hook_response)

    def test_restricted_error_redirects_to_delete_url(self):
        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError("restricted", {self.restricted_obj}),
        ):
            with patch("core.views.reverse", side_effect=NoReverseMatch):
                response = self.view.form_valid(MagicMock())

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/delete/")

    def test_restricted_error_shows_error_message(self):
        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError("restricted", {self.restricted_obj}),
        ):
            with patch("core.views.reverse", side_effect=NoReverseMatch):
                self.view.form_valid(MagicMock())

        msgs = self._get_messages()
        self.assertTrue(
            any("Cannot delete — model instance referenced by:" in m for m in msgs)
        )

    def test_restricted_error_no_success_message(self):
        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError("restricted", {self.restricted_obj}),
        ):
            with patch("core.views.reverse", side_effect=NoReverseMatch):
                self.view.form_valid(MagicMock())

        msgs = self._get_messages()
        self.assertNotIn("Deleted successfully.", msgs)

    def test_restricted_error_message_contains_model_name(self):
        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError("restricted", {self.restricted_obj}),
        ):
            with patch("core.views.reverse", side_effect=NoReverseMatch):
                self.view.form_valid(MagicMock())

        msgs = self._get_messages()
        self.assertTrue(any("Related Items" in m for m in msgs))

    def test_restricted_error_message_contains_edit_link_when_reverse_succeeds(self):
        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError("restricted", {self.restricted_obj}),
        ):
            with patch("core.views.reverse", return_value="/edit/99/"):
                self.view.form_valid(MagicMock())

        msgs = self._get_messages()
        self.assertTrue(any('<a href="/edit/99/">' in m for m in msgs))

    def test_error_message_falls_back_to_plain_text_on_no_reverse_match(self):
        self.restricted_obj.__str__ = MagicMock(return_value="Related Item 1")

        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError("restricted", {self.restricted_obj}),
        ):
            with patch("core.views.reverse", side_effect=NoReverseMatch):
                self.view.form_valid(MagicMock())

        msgs = self._get_messages()
        self.assertTrue(any("Related Item 1" in m for m in msgs))
        self.assertFalse(any("<a href" in m for m in msgs))

    def test_multiple_restricted_objects_all_appear_in_message(self):
        restricted_obj1 = self._make_restricted_obj(
            "related items", "core", "relatedmodel", pk=1
        )
        restricted_obj2 = self._make_restricted_obj(
            "related items", "core", "relatedmodel", pk=2
        )
        # Force same class so they group together
        restricted_obj2.__class__ = restricted_obj1.__class__

        with patch.object(
            CustomSnippetDeleteView,
            "delete_action",
            side_effect=RestrictedError(
                "restricted", {restricted_obj1, restricted_obj2}
            ),
        ):
            with patch("core.views.reverse", side_effect=NoReverseMatch):
                self.view.form_valid(MagicMock())

        msgs = self._get_messages()
        print("msgs: ", msgs)
        self.assertTrue(
            any(
                "relatedmodel object (1)" in m and "relatedmodel object (2)" in m
                for m in msgs
            )
        )
