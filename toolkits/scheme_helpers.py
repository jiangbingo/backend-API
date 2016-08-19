# -*- encoding: utf-8 -*-
from django.core.cache import cache
from django.db.models import Q
from account_helpers import create_or_get_other_account
from models.models import Macro, MacroBrand
from django.conf import settings


def save_brick(**kwargs):
    type = Macro.TYPE_BRICK
    account = kwargs['account']
    username = kwargs['username']
    other_account = create_or_get_other_account(account, username)
    paving_id = kwargs['paving_id'][0]
    paving_name = kwargs['paving_name'][0]
    cnf_name = kwargs['cnf_name'][0]
    style_id = kwargs['style_id'][0]
    brand_ids = kwargs['brand_id_set'][0].split(',')
    suitable_material = kwargs['suitable_material'][0]
    cnf_body = kwargs['cnf_body'][0]
    img = kwargs['img'][0]
    is_share = int(kwargs['is_share'][0])
    macro = Macro(account=account, other_account=other_account,
                  paving_id=paving_id, paving_name=paving_name,
                  cnf_name=cnf_name, style_id=style_id,
                  suitable_material=suitable_material, is_share=is_share,
                  type=type)
    macro.cnf_body.save(name=cnf_body.name, content=cnf_body)
    macro.img.save(name=img.name, content=img)
    macro.save()
    macro_brand_array = []
    for brand_id in brand_ids:
        macro_brand_array.append(MacroBrand(macro=macro, brand_id=brand_id))
    MacroBrand.objects.bulk_create(macro_brand_array)
    return {'status': 1, 'info': 'success', 'data': macro.id}


def get_bricks(**kwargs):
    account = kwargs['account']
    username = kwargs['username']
    paving_id = 0
    if kwargs.get('paving_id'):
        paving_id = kwargs['paving_id'][0]
    top = 0
    if kwargs.get('top'):
        top = int(kwargs['top'][0])
    suitable = ''
    if kwargs.get('suitable'):
        suitable = kwargs['suitable'][0]
    type = ''
    if kwargs.get('type'):
        type = kwargs['type'][0]
    paving_q = Q()
    if paving_id:
        paving_q = Q(paving_id=paving_id)
    suitable_q = Q()
    if suitable:
        suitable_q = Q(suitable_material__icontains=suitable)
    type_q = Q(account=account, other_account__username=username)
    if type.lower() == 'a':
        type_q = Q(account__isnull=True, other_account__isnull=True)
    elif type.lower() == 'b':
        type_q = Q(account=account, is_share=True)
    elif type.lower() == 'c':
        type_q = Q(account=account, is_share=True, other_account__isnull=True)
    macros = Macro.objects.prefetch_related('brands').filter(paving_q,
                                                             suitable_q, type_q,
                                                             type=Macro.TYPE_BRICK,
                                                             active=True)
    result = []
    for macro in macros:
        brands = macro.brands.all()
        img_url = ''
        if macro.img:
            img_url = settings.HOST + macro.img.url
        result.append({
            'cnf_id': macro.id,
            'paving_id': macro.paving_id,
            'paving_name': macro.paving_name,
            'cnf_name': macro.cnf_name,
            'style_id': macro.style_id,
            'brand_id_set': ','.join([('%s' % brand.id) for brand in brands]),
            'brand_name_set': ','.join([brand.name for brand in brands]),
            'suitable_material': macro.suitable_material,
            'img': img_url
        })
    return {'status': 1, 'info': 'success', 'data': result}


def get_brick(**kwargs):
    cnf_id = kwargs['cnf_id'][0]
    macro = Macro.objects.get(pk=cnf_id)
    body_url = ''
    if macro.cnf_body:
        body_url = settings.HOST + macro.cnf_body.url
    macro_dict = {
        'cnf_id': macro.id,
        'paving_id': macro.paving_id,
        'paving_name': macro.paving_name,
        'cnf_name': macro.cnf_name,
        'suitable_material': macro.suitable_material,
        'cnf_body': body_url
    }
    return {'status': 1, 'info': 'success', 'data': macro_dict}


def save_line(**kwargs):
    type = Macro.TYPE_LINE
    account = kwargs['account']
    username = kwargs['username']
    other_account = create_or_get_other_account(account, username)
    paving_id = kwargs['paving_id'][0]
    paving_name = kwargs['paving_name'][0]
    cnf_name = kwargs['cnf_name'][0]
    cnf_type = kwargs['cnf_type'][0]
    style_id = kwargs['style_id'][0]
    brand_ids = kwargs['brand_id_set'][0].split(',')
    suitable_material = kwargs['suitable_material'][0]
    cnf_body = kwargs['cnf_body'][0]
    img = kwargs['img'][0]
    is_share = int(kwargs['is_share'][0])
    macro = Macro(account=account, other_account=other_account,
                  paving_id=paving_id, paving_name=paving_name,
                  cnf_name=cnf_name, cnf_type=cnf_type, style_id=style_id,
                  suitable_material=suitable_material, is_share=is_share,
                  type=type)
    macro.cnf_body.save(name=cnf_body.name, content=cnf_body)
    macro.img.save(name=img.name, content=img)
    macro.save()
    macro_brand_array = []
    for brand_id in brand_ids:
        macro_brand_array.append(MacroBrand(macro=macro, brand_id=brand_id))
    MacroBrand.objects.bulk_create(macro_brand_array)
    return {'status': 1, 'info': 'success', 'data': macro.id}


def get_lines(**kwargs):
    account = kwargs['account']
    username = kwargs['username']
    cnf_type = kwargs['cnf_type'][0]
    paving_id = 0
    if kwargs.get('paving_id'):
        paving_id = kwargs['paving_id'][0]
    top = 0
    if kwargs.get('top'):
        top = int(kwargs['top'][0])
    suitable = ''
    if kwargs.get('suitable'):
        suitable = kwargs['suitable'][0]
    type = ''
    if kwargs.get('type'):
        type = kwargs['type'][0]
    paving_q = Q()
    if paving_id:
        paving_q = Q(paving_id=paving_id)
    suitable_q = Q()
    if suitable:
        suitable_q = Q(suitable_material__icontains=suitable)
    type_q = Q(account=account, other_account__username=username)
    if type.lower() == 'a':
        type_q = Q(account__isnull=True, other_account__isnull=True)
    elif type.lower() == 'b':
        type_q = Q(account=account, is_share=True)
    elif type.lower() == 'c':
        type_q = Q(account=account, is_share=True, other_account__isnull=True)
    macros = Macro.objects.prefetch_related('brands').filter(paving_q,
                                                             suitable_q, type_q,
                                                             cnf_type=cnf_type,
                                                             type=Macro.TYPE_LINE,
                                                             active=True)
    result = []
    for macro in macros:
        brands = macro.brands.all()
        img_url = ''
        if macro.img:
            img_url = settings.HOST + macro.img.url
        result.append({
            'cnf_id': macro.id,
            'paving_id': macro.paving_id,
            'paving_name': macro.paving_name,
            'cnf_type': macro.cnf_type,
            'cnf_name': macro.cnf_name,
            'style_id': macro.style_id,
            'brand_id_set': ','.join([('%s' % brand.id) for brand in brands]),
            'brand_name_set': ','.join([brand.name for brand in brands]),
            'suitable_material': macro.suitable_material,
            'img': img_url
        })
    return {'status': 1, 'info': 'success', 'data': result}


def get_line(**kwargs):
    cnf_id = kwargs['cnf_id'][0]
    macro = Macro.objects.get(pk=cnf_id)
    body_url = ''
    if macro.cnf_body:
        body_url = settings.HOST + macro.cnf_body.url
    macro_dict = {
        'cnf_id': macro.id,
        'paving_id': macro.paving_id,
        'paving_name': macro.paving_name,
        'cnf_name': macro.cnf_name,
        'suitable_material': macro.suitable_material,
        'cnf_body': body_url
    }
    return {'status': 1, 'info': 'success', 'data': macro_dict}


def save_parquet(**kwargs):
    type = Macro.TYPE_PARQUET
    account = kwargs['account']
    username = kwargs['username']
    other_account = create_or_get_other_account(account, username)
    paving_id = kwargs['paving_id'][0]
    paving_name = kwargs['paving_name'][0]
    cnf_name = kwargs['cnf_name'][0]
    style_id = kwargs['style_id'][0]
    brand_ids = kwargs['brand_id_set'][0].split(',')
    suitable_material = kwargs['suitable_material'][0]
    cnf_body = kwargs['cnf_body'][0]
    img = kwargs['img'][0]
    is_share = int(kwargs['is_share'][0])
    macro = Macro(account=account, other_account=other_account,
                  paving_id=paving_id, paving_name=paving_name,
                  cnf_name=cnf_name, style_id=style_id,
                  suitable_material=suitable_material,
                  is_share=is_share, type=type)
    macro.cnf_body.save(name=cnf_body.name, content=cnf_body)
    macro.img.save(name=img.name, content=img)
    macro.save()
    macro_brand_array = []
    for brand_id in brand_ids:
        macro_brand_array.append(MacroBrand(macro=macro, brand_id=brand_id))
    MacroBrand.objects.bulk_create(macro_brand_array)
    return {'status': 1, 'info': 'success', 'data': macro.id}


def get_parquets(**kwargs):
    account = kwargs['account']
    username = kwargs['username']
    paving_id = 0
    if kwargs.get('paving_id'):
        paving_id = kwargs['paving_id'][0]
    top = 0
    if kwargs.get('top'):
        top = int(kwargs['top'][0])
    suitable = ''
    if kwargs.get('suitable'):
        suitable = kwargs['suitable'][0]
    type = ''
    if kwargs.get('type'):
        type = kwargs['type'][0]
    paving_q = Q()
    if paving_id:
        paving_q = Q(paving_id=paving_id)
    suitable_q = Q()
    if suitable:
        suitable_q = Q(suitable_material__icontains=suitable)
    type_q = Q(account=account, other_account__username=username)
    if type.lower() == 'a':
        type_q = Q(account__isnull=True, other_account__isnull=True)
    elif type.lower() == 'b':
        type_q = Q(account=account, is_share=True)
    elif type.lower() == 'c':
        type_q = Q(account=account, is_share=True, other_account__isnull=True)
    macros = Macro.objects.prefetch_related('brands').filter(paving_q,
                                                             suitable_q, type_q,
                                                             type=Macro.TYPE_PARQUET,
                                                             active=True)
    result = []
    for macro in macros:
        brands = macro.brands.all()
        img_url = ''
        if macro.img:
            img_url = settings.HOST + macro.img.url
        result.append({
            'cnf_id': macro.id,
            'paving_id': macro.paving_id,
            'paving_name': macro.paving_name,
            'cnf_type': macro.cnf_type,
            'cnf_name': macro.cnf_name,
            'style_id': macro.style_id,
            'brand_id_set': ','.join([('%s' % brand.id) for brand in brands]),
            'brand_name_set': ','.join([brand.name for brand in brands]),
            'suitable_material': macro.suitable_material,
            'img': img_url
        })
    return {'status': 1, 'info': 'success', 'data': result}


def get_parquet(**kwargs):
    cnf_id = kwargs['cnf_id'][0]
    macro = Macro.objects.get(pk=cnf_id)
    body_url = ''
    if macro.cnf_body:
        body_url = settings.HOST + macro.cnf_body.url
    macro_dict = {
        'cnf_id': macro.id,
        'paving_id': macro.paving_id,
        'paving_name': macro.paving_name,
        'cnf_name': macro.cnf_name,
        'suitable_material': macro.suitable_material,
        'cnf_body': body_url
    }
    return {'status': 1, 'info': 'success', 'data': macro_dict}


def save_wall(**kwargs):
    type = Macro.TYPE_WALL
    account = kwargs['account']
    username = kwargs['username']
    other_account = create_or_get_other_account(account, username)
    cnf_name = kwargs['cnf_name'][0]
    style_id = kwargs['style_id'][0]
    cnf_body = kwargs['cnf_body'][0]
    img = kwargs['img'][0]
    is_share = int(kwargs['is_share'][0])
    macro = Macro(account=account, other_account=other_account,
                  cnf_name=cnf_name, style_id=style_id, is_share=is_share,
                  type=type)
    macro.img.save(name=cnf_body.name, content=cnf_body)
    macro.img.save(name=img.name, content=img)
    macro.save()
    return {'status': 1, 'info': 'success', 'data': macro.id}


def get_walls(**kwargs):
    account = kwargs['account']
    username = kwargs['username']
    keyword = 0
    if kwargs.get('keyword'):
        keyword = kwargs['keyword'][0]
    style_id = 0
    if kwargs.get('top'):
        style_id = int(kwargs['style_id'][0])
    type = ''
    if kwargs.get('type'):
        type = kwargs['type'][0]
    keyword_q = Q()
    if keyword:
        keyword_q = Q(cnf_name__icontains=keyword)
    style_q = Q()
    if style_id:
        style_q = Q(style_id=style_id)
    type_q = Q(account=account, other_account__username=username)
    if type.lower() == 'a':
        type_q = Q(account__isnull=True, other_account__isnull=True)
    elif type.lower() == 'b':
        type_q = Q(account=account, is_share=True)
    elif type.lower() == 'c':
        type_q = Q(account=account, is_share=True, other_account__isnull=True)
    macros = Macro.objects.prefetch_related('brands').filter(keyword_q, style_q,
                                                             type_q,
                                                             type=Macro.TYPE_WALL,
                                                             active=True)
    result = []
    for macro in macros:
        img_url = ''
        if macro.img:
            img_url = settings.HOST + macro.img.url
        result.append({
            'cnf_id': macro.id,
            'cnf_name': macro.cnf_name,
            'style_id': macro.style_id,
            'img': img_url
        })
    return {'status': 1, 'info': 'success', 'data': result}


def get_wall(**kwargs):
    cnf_id = kwargs['cnf_id'][0]
    macro = Macro.objects.get(pk=cnf_id)
    body_url = ''
    if macro.cnf_body:
        body_url = settings.HOST + macro.cnf_body.url
    macro_dict = {
        'cnf_id': macro.id,
        'cnf_name': macro.cnf_name,
        'cnf_body': body_url
    }
    return {'status': 1, 'info': 'success', 'data': macro_dict}


def save_room(**kwargs):
    type = Macro.TYPE_ROOM
    account = kwargs['account']
    username = kwargs['username']
    other_account = create_or_get_other_account(account, username)
    room_type_id = kwargs['room_type_id'][0]
    cnf_name = kwargs['cnf_name'][0]
    style_id = kwargs['style_id'][0]
    cnf_body = kwargs['cnf_body'][0]
    edge = kwargs['edge'][0]
    img = kwargs['img'][0]
    is_share = int(kwargs['is_share'][0])
    macro = Macro(account=account, other_account=other_account,
                  cnf_name=cnf_name, style_id=style_id, edge=edge,
                  paving_id=room_type_id,
                  is_share=is_share, type=type)
    macro.img.save(name=cnf_body.name, content=cnf_body)
    macro.img.save(name=img.name, content=img)
    macro.save()
    return {'status': 1, 'info': 'success', 'data': macro.id}


def get_rooms(**kwargs):
    account = kwargs['account']
    username = kwargs['username']
    keyword = 0
    if kwargs.get('keyword'):
        keyword = kwargs['keyword'][0]
    style_id = 0
    style_q = Q()
    if kwargs.get('top'):
        style_id = int(kwargs['style_id'][0])
    type = ''
    if kwargs.get('type'):
        type = kwargs['type'][0]
    room_type_id = 0
    if kwargs.get('room_type_id'):
        room_type_id = kwargs['room_type_id'][0]
    keyword_q = Q()
    if keyword:
        keyword_q = Q(cnf_name__icontains=keyword)
    if style_id:
        style_id = Q(style_id=style_id)
    type_q = Q(account=account, other_account__username=username)
    if type.lower() == 'a':
        type_q = Q(account__isnull=True, other_account__isnull=True)
    elif type.lower() == 'b':
        type_q = Q(account=account, is_share=True)
    elif type.lower() == 'c':
        type_q = Q(account=account, is_share=True, other_account__isnull=True)
    room_type_q = Q()
    if room_type_id:
        room_type_q = Q(paving_id=room_type_id)
    macros = Macro.objects.prefetch_related('brands').filter(keyword_q, style_q,
                                                             type_q,
                                                             room_type_q,
                                                             type=Macro.TYPE_ROOM,
                                                             active=True)
    result = []
    for macro in macros:
        brands = macro.brands.all()
        img_url = ''
        if macro.img:
            img_url = settings.HOST + macro.img.url
        result.append({
            'cnf_id': macro.id,
            'cnf_name': macro.cnf_name,
            'style_id': macro.style_id,
            'room_type_id': macro.paving_id,
            'img': img_url
        })
    return {'status': 1, 'info': 'success', 'data': result}


def get_room(**kwargs):
    cnf_id = kwargs['cnf_id'][0]
    macro = Macro.objects.get(pk=cnf_id)
    body_url = ''
    if macro.cnf_body:
        body_url = settings.HOST + macro.cnf_body.url
    macro_dict = {
        'cnf_id': macro.id,
        'cnf_name': macro.cnf_name,
        'cnf_body': body_url
    }
    return {'status': 1, 'info': 'success', 'data': macro_dict}
