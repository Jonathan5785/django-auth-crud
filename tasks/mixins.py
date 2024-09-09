from django.contrib.auth.mixins import UserPassesTestMixin

class UserIsAdminMixin(UserPassesTestMixin):
    def test_func(self) -> bool:
        return self.request.user.is_admin
    