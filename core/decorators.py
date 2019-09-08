from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test


def cooperative_member_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_authenticated and u.is_cooperative_member,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def active_member_required(function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url='home'):
    actual_decorator = user_passes_test(
        lambda u: u.is_active and u.is_authenticated and (u.is_cooperative_member or u.is_partner),
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
