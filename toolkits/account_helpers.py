# -*- encoding: utf-8 -*-
from django.core.cache import cache
from django.db.models import Q
from models.models import Province, City, Area, Property, Apartment, OtherAccount
from django.conf import settings
def login(**kwargs):
    return {
        "status": 1,
        "info": "success",
        "data": {
            "userid":'2',
            "username":'spacemaster',
            "headimg":''

        }
    }


def get_provinces(**kwargs):
    province_array = cache.get('cities')

    if not province_array:
        provinces = Province.objects.prefetch_related('cities','cities__areas').all()
        province_array = []
        for province in provinces:
            city = province.cities.all().first()
            city_dict = {}
            if city:
                area = city.areas.all().first()
                area_dict = {}
                if area:
                    area_dict = {
                        'id':area.id,
                        'parent_id':city.id,
                        'name':area.fullname,
                        'short':area.fullname,
                        'letter':'',
                        'level':3
                    }
                city_dict = {
                    'id': city.id,
                    'parent_id': province.id,
                    'name': city.fullname,
                    'short': city.name,
                    'letter': city.pinyin,
                    'level': 2,
                    'region': area_dict
                }
            province_dict = {
                'id':province.id,
                'parent_id':0,
                'name':province.fullname,
                'short':province.name,
                'letter':province.pinyin,
                'level':1,
                'city':city_dict
            }
            province_array.append(province_dict)
            cache.set('cities',province_array)
    return {'success':1,'info':'success','data':province_array}

def get_properties(**kwargs):
    properties_array = []
    limit = 20
    if kwargs.get('limit'):
        limit = int(kwargs['limit'][0])
    province = ''
    if kwargs.get('province'):
        province = kwargs['province'][0]
    city = ''
    if kwargs.get('city'):
        city = kwargs['city'][0]
    name = ''
    if kwargs.get('name'):
        name = kwargs['name'][0]
    province_q = Q()
    if province:
        province_q = Q(province=province)
    city_q = Q()
    if city:
        city_q = Q(city=city)
    name_q = Q()
    if name:
        name_q = Q(name__icontains=name)
    properties = Property.objects.filter(province_q,city_q,name_q,active=True)[:limit]
    for property in properties:
        properties_array.append({'id':property.id,'name':property.name})
    return {'success': 1, 'info': 'success', 'data': properties_array}


def get_apartments(**kwargs):
    apartments_array = []
    city = ''
    if kwargs.get('city'):
        city = kwargs['city'][0]
    property = ''
    if kwargs.get('property'):
        property = kwargs['property'][0]
    is_empty = False
    if kwargs.get('is_empty'):
        is_empty = kwargs['is_empty'][0] == '1'
    keyword = ''
    if kwargs.get('keyword'):
        keyword = kwargs['keyword'][0]
    type = 1
    if kwargs.get('type'):
        type = int(kwargs['type'][0])
    apartment = ''
    if kwargs.get('apartment'):
        apartment = int(kwargs['apartment'][0])
    else:
        if type == 2:
            return {'success': 0, 'info': '参数apartment为必传', 'data': []}
    city_q = Q()
    if city:
        city_q = Q(property__city=city)
    property_q = Q()
    if property:
        property_q = Q(property=property)
    keyword_q = Q()
    if keyword:
        keyword_q = Q(name__icontains=keyword)
    apartment_q = Q()
    if type==2 and apartment:
        apartment_q = Q(pk=apartment)
    apartments =Apartment.objects.filter(city_q,property_q,keyword_q,apartment_q,active=True)
    for apartment in apartments:
        apartments_array.append({
            'id':apartment.id,
            'name':apartment.name,
            'graph':'0',
            'image':settings.HOST + apartment.preview.url,
            'area':apartment.acreage,
            'room_num':apartment.room_count,
            'hall_num':apartment.hall_count,
            'kitchen_num':apartment.kitchen_count,
            'toilet_num':apartment.restroom_count,
            'balcony_num':0
        })

    return {'success': 1, 'info': 'success', 'data': apartments_array}

def create_or_get_other_account(account, username):
    if account.role == 1:
        return None
    else:
        other_account,flag = OtherAccount.objects.get_or_create(platform=account,username=username)
        return other_account