# -*- encoding:utf-8 -*-
from django.db import transaction
from urllib import unquote
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from rest_framework import status
from models.models import AccountKey
from toolkits.rsa_tools import RsaServer
from django.core.cache import cache

class AuthorizeMixin(object):
    def dispatch(self, request, *args, **kwargs):
        # mod = request.GET.get('mod')
        # act = request.GET.get('act')
        # if mod == '100' and act == '2':
        #     return super(AuthorizeMixin, self).dispatch(request, *args,
        #                                                 **kwargs)
        # sessionid = request.META.get('HTTP_SID', request.COOKIES.get('sessionid',''))
        # if not sessionid:
        #     if request.is_ajax():
        #         return HttpResponse(
        #             {'status': 0, 'info': '没有权限', 'data': []},
        #             status=status.HTTP_403_FORBIDDEN)
        #     else:
        #         raise PermissionDenied
        # session_data = cache.get(sessionid)
        # if not session_data:
        #     if request.is_ajax():
        #         return HttpResponse(
        #             {'status': 0, 'info': '没有权限', 'data': []},
        #             status=status.HTTP_403_FORBIDDEN)
        #     else:
        #         raise PermissionDenied
        # if session_data:
        #     username = session_data.get('username')
        #     sec_data = session_data.get('sec_data')
        #
        #     uid = session_data.get('uid')
        #     sid = session_data.get('sid')
        #     source = session_data.get('source')
        #     session_args = session_data.get('args')
        #     if not sec_data:
        #         if request.is_ajax():
        #             return HttpResponse(
        #                 {'status': 0, 'info': '没有权限', 'data': []},
        #                 status=status.HTTP_403_FORBIDDEN)
        #         else:
        #             raise PermissionDenied
        #     account_key =  AccountKey.objects.select_related('account').filter(
        #         app_secret=sec_data).first()
        #     if not account_key:
        #         if request.is_ajax():
        #             return HttpResponse(
        #                 {'status': 0, 'info': '没有权限', 'data': []},
        #                 status=status.HTTP_403_FORBIDDEN)
        #         else:
        #             raise PermissionDenied
        #     account = account_key.account
        #     request.account = account
        #     request.username = username
        #     request.source = source
        #     if uid:
        #         request.uid = uid
        return super(AuthorizeMixin, self).dispatch(request, *args, **kwargs)

    def ck(self, request_data):
        app_secret = request_data.get("sec_data", None)
        key = None
        keys = AccountKey.objects.filter(
            app_secret=app_secret)
        if keys.exists():
            key = keys[0]
            data = key.token + key.license + key.app_secret
            license = key.license
        else:
            return None
        result = RsaServer.check(data, request_data.get("sign", None))
        # print "result", result
        out = self._token_check(license)
        if result and out:
            return key
        else:
            return None

    def _token_check(self, data):
        # 匹配权限
        return True


class AtomicMixin(object):
    """
    Ensures we rollback db transactions on exceptions.
    Idea from https://github.com/tomchristie/django-rest-framework/pull/1204
    """

    @transaction.atomic()
    def dispatch(self, *args, **kwargs):
        return super(AtomicMixin, self).dispatch(*args, **kwargs)

    def handle_exception(self, *args, **kwargs):
        response = super(AtomicMixin, self).handle_exception(*args, **kwargs)

        if getattr(response, 'exception'):
            # We've suppressed the exception but still need to rollback any transaction.
            transaction.set_rollback(True)

        return response
