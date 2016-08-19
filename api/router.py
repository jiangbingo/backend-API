# -*- encoding: utf-8 -*-
from rest_framework import viewsets
from toolkits.mixins import AtomicMixin, AuthorizeMixin
from rest_framework.response import Response
from rest_framework import status
from rest_framework.routers import BaseRouter, Route, DynamicListRoute, \
    DynamicDetailRoute, flatten, replace_methodname
from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import url

from toolkits.products_helpers import *
from toolkits.account_helpers import *
from toolkits.scheme_helpers import *


class APIRouter(BaseRouter):
    routes = [
        # List route.
        Route(
            url=r'^{prefix}{trailing_slash}$',
            mapping={
                'get': 'get',
                'post': 'post',
                'options': 'post'
            },
            name='{basename}-list',
            initkwargs={'suffix': 'List'}
        ),
        # Dynamically generated list routes.
        # Generated using @list_route decorator
        # on methods of the viewset.
        DynamicListRoute(
            url=r'^{prefix}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
        # Detail route.
        Route(
            url=r'^{prefix}/{lookup}{trailing_slash}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            initkwargs={'suffix': 'Instance'}
        ),
        # Dynamically generated detail routes.
        # Generated using @detail_route decorator on methods of the viewset.
        DynamicDetailRoute(
            url=r'^{prefix}/{lookup}/{methodname}{trailing_slash}$',
            name='{basename}-{methodnamehyphen}',
            initkwargs={}
        ),
    ]

    def __init__(self, trailing_slash=True):
        self.trailing_slash = trailing_slash and '/' or ''
        super(APIRouter, self).__init__()

    def get_default_base_name(self, viewset):
        """
        If `base_name` is not specified, attempt to automatically determine
        it from the viewset.
        """
        queryset = getattr(viewset, 'queryset', None)

        assert queryset is not None, '`base_name` argument not specified, and could ' \
                                     'not automatically determine the name from the viewset, as ' \
                                     'it does not have a `.queryset` attribute.'

        return queryset.model._meta.object_name.lower()

    def get_routes(self, viewset):
        """
        Augment `self.routes` with any dynamically generated routes.

        Returns a list of the Route namedtuple.
        """

        known_actions = flatten(
            [route.mapping.values() for route in self.routes if
             isinstance(route, Route)])

        # Determine any `@detail_route` or `@list_route` decorated methods on the viewset
        detail_routes = []
        list_routes = []
        for methodname in dir(viewset):
            attr = getattr(viewset, methodname)
            httpmethods = getattr(attr, 'bind_to_methods', None)
            detail = getattr(attr, 'detail', True)
            if httpmethods:
                if methodname in known_actions:
                    raise ImproperlyConfigured(
                        'Cannot use @detail_route or @list_route '
                        'decorators on method "%s" '
                        'as it is an existing route' % methodname)
                httpmethods = [method.lower() for method in httpmethods]
                if detail:
                    detail_routes.append((httpmethods, methodname))
                else:
                    list_routes.append((httpmethods, methodname))

        def _get_dynamic_routes(route, dynamic_routes):
            ret = []
            for httpmethods, methodname in dynamic_routes:
                method_kwargs = getattr(viewset, methodname).kwargs
                initkwargs = route.initkwargs.copy()
                initkwargs.update(method_kwargs)
                url_path = initkwargs.pop("url_path", None) or methodname
                ret.append(Route(
                    url=replace_methodname(route.url, url_path),
                    mapping={httpmethod: methodname for httpmethod in
                             httpmethods},
                    name=replace_methodname(route.name, url_path),
                    initkwargs=initkwargs,
                ))

            return ret

        ret = []
        for route in self.routes:
            if isinstance(route, DynamicDetailRoute):
                # Dynamic detail routes (@detail_route decorator)
                ret += _get_dynamic_routes(route, detail_routes)
            elif isinstance(route, DynamicListRoute):
                # Dynamic list routes (@list_route decorator)
                ret += _get_dynamic_routes(route, list_routes)
            else:
                # Standard route
                ret.append(route)

        return ret

    def get_method_map(self, viewset, method_map):
        """
        Given a viewset, and a mapping of http methods to actions,
        return a new mapping which only includes any mappings that
        are actually implemented by the viewset.
        """
        bound_methods = {}
        for method, action in method_map.items():
            if hasattr(viewset, action):
                bound_methods[method] = action
        return bound_methods

    def get_lookup_regex(self, viewset, lookup_prefix=''):
        """
        Given a viewset, return the portion of URL regex that is used
        to match against a single instance.

        Note that lookup_prefix is not used directly inside REST rest_framework
        itself, but is required in order to nicely support nested router
        implementations, such as drf-nested-routers.

        https://github.com/alanjds/drf-nested-routers
        """
        base_regex = '(?P<{lookup_prefix}{lookup_url_kwarg}>{lookup_value})'
        # Use `pk` as default field, unset set.  Default regex should not
        # consume `.json` style suffixes and should break at '/' boundaries.
        lookup_field = getattr(viewset, 'lookup_field', 'pk')
        lookup_url_kwarg = getattr(viewset, 'lookup_url_kwarg',
                                   None) or lookup_field
        lookup_value = getattr(viewset, 'lookup_value_regex', '[^/.]+')
        return base_regex.format(
            lookup_prefix=lookup_prefix,
            lookup_url_kwarg=lookup_url_kwarg,
            lookup_value=lookup_value
        )

    def get_urls(self):
        """
        Use the registered viewsets to generate a list of URL patterns.
        """
        ret = []

        for prefix, viewset, basename in self.registry:
            lookup = self.get_lookup_regex(viewset)
            routes = self.get_routes(viewset)

            for route in routes:

                # Only actions which actually exist on the viewset will be bound
                mapping = self.get_method_map(viewset, route.mapping)
                if not mapping:
                    continue

                # Build the url pattern
                regex = route.url.format(
                    prefix=prefix,
                    lookup=lookup,
                    trailing_slash=self.trailing_slash
                )
                view = viewset.as_view(mapping, **route.initkwargs)
                name = route.name.format(basename=basename)
                ret.append(url(regex, view, name=name))

        return ret


function_map = {'1': {'1': 'get_hardness_categories',
                      '2': 'get_conditions',
                      '3': 'get_series',
                      '4': 'get_model_data',
                      '5': 'get_model_texture'},
                '2': {'1': 'get_categories',
                      '2': 'get_conditions',
                      '3': 'get_series',
                      '4': 'get_model_data',
                      '5': 'get_model_texture'},
                '3': {'1': '',
                      '2': '',
                      '3': '',
                      '4': ''},
                '4': {'1': '',
                      '2': '',
                      '3': '',
                      '4': ''},
                '5': {'1': '',
                      '2': '',
                      '3': '',
                      '4': ''},
                '6': {'1': 'save_brick',
                      '2': 'get_bricks',
                      '3': 'get_brick'},
                '7': {'1': 'save_line',
                      '2': 'get_lines',
                      '3': 'get_line'},
                '8': {'1': 'save_parquet',
                      '2': 'get_parquets',
                      '3': 'get_parquet'},
                '9': {'1': 'save_wall',
                      '2': 'get_walls',
                      '3': 'get_wall'},
                '10': {'1': 'save_room',
                       '2': 'get_rooms',
                       '3': 'get_room'},
                '11': {'1': '',
                       '2': '',
                       '3': '',
                       '4': '',
                       '5': ''},
                '12': {'1': ''},
                '100': {'1': '',
                        '2': 'login',
                        '3': 'get_provinces',
                        '4': 'get_properties',
                        '5': 'get_apartments',
                        '6': '',
                        '7': '',
                        '8': '',
                        '9': '',
                        '10': '',
                        '11': ''},
                '101': {'1': '',
                        '2': '',
                        '3': '',
                        '4': '',
                        '5': '',
                        '6': '',
                        '7': '',
                        '8': '',
                        '9': '',
                        '10': '',
                        '11': '',
                        '12': ''}}

class MasterViewSet(AuthorizeMixin, AtomicMixin,
                    viewsets.ViewSet):
    def get(self, request):
        return self.post(request)

    def post(self, request):
        '''
        入口，http://host:port/master?mode=1&act=1
        '''
        mod = request.GET.get('mod')
        act = request.GET.get('act')
        if not mod or not act:
            return Response({'status': 0, 'info': '参数不正确', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        if not function_map.get(mod):
            return Response({'status': 0, 'info': '参数mod不正确', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        if not function_map[mod].get(act):
            return Response({'status': 0, 'info': '参数act不正确', 'data': []},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            kwargs = dict(request.data)
            if hasattr(request, 'account'):
                kwargs.update({'account': request.account})
            if hasattr(request, 'username'):
                kwargs.update({'username':request.username})
            result = eval(function_map[mod][act])(**kwargs)
        except Exception as e:
            result = {'status': 0, 'info': e.message, 'data': []}
        return Response(result,
                        status=status.HTTP_200_OK)
