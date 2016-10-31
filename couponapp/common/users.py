

__all__ = [
        'user_in_a_group',
        'get_name',
        'all_permissions_required',
        ]


from functools import update_wrapper, wraps

from django.contrib.auth.decorators import permission_required
from django.utils.translation import ugettext_lazy as _


def user_in_a_group(user, groups):
    """\
    This takes a User and a QuerySet of Group objects and tests whether the
    user is in one of these groups.

    """

    user_groups = set( g.pk for g in user.groups.all() )
    group_set = set( g.pk for g in groups.all() )
    return not user_groups.isdisjoint(group_set)


def get_name(user):
    if user.is_authenticated():
        return user.get_full_name() or user.username
    else:
        return _(u'guest')


def all_permissions_required(*perms):
    """\
    This is a decorator that expands to a series of permission_required calls.

    For example:

        @permission_required('a')
        @permission_required('b')
        def f():
            pass

    can be rewritten as

        @all_permissions_required('a', 'b')
        def f():
            pass

    """

    perm_decorators = [ permission_required(p) for p in perms ]
    def decorator(f):
        wrapped = f
        for p in perm_decorators:
            wrapped = update_wrapper(p(wrapped), f)
        return wrapped
    return decorator


