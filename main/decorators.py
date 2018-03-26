from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.urlresolvers import reverse_lazy


def staff_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=reverse_lazy('main:login')):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_staff,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator