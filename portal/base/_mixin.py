from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseRedirect
from django.urls import reverse

class SuperUserMixin(LoginRequiredMixin, UserPassesTestMixin):
    permission_denied_message = 'You must select an issuer.'

    def test_func(self):
        return self.request.user.is_superuser

    def handle_no_permission(self):
        return HttpResponseRedirect(reverse("no-permission"))