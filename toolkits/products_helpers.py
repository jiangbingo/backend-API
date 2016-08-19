# -*- encoding: utf-8 -*-
from models.models import ProductCategory, ProductBrand, ProductBrandSeries, \
    Product, Manufactor
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Q
from django.core.cache import cache


def get_hardness_categories(**kwargs):
    result = cache.get('hardness_categories')
    if not result:
        print 'select'
        res = []
        for c1 in ProductCategory.objects.prefetch_related('sub_categories',
                                                           'sub_categories__sub_categories').filter(
            step=2, active=True, name__in=['门','窗','硬件构造']):
            c1_dict = {
                "id": c1.id,
                "name": c1.name,
                'tag': c1.name,
                "list": []
            }
            res.append(c1_dict)
            for c2 in c1.sub_categories.all():
                if not c2.active:
                    continue
                c2_dict = {
                    "id": c2.id,
                    "name": c2.name,
                }
                c1_dict['list'].append(c2_dict)
        cache.set('hardness_categories', res)
        result = res
    return {'status': 1, 'info': 'success', 'data': result}


def get_categories(**kwargs):
    '''
    返回房间硬装分类
    '''
    result = cache.get('categories')
    if not result:
        print 'select'
        res = []
        for c1 in ProductCategory.objects.prefetch_related('sub_categories',
                                                           'sub_categories__sub_categories').filter(
            step=1, active=True):
            c1_dict = {
                "id": c1.id,
                "name": c1.name,
                'tag': c1.name,
                "list": []
            }
            res.append(c1_dict)
            for c2 in c1.sub_categories.all():
                if not c2.active:
                    continue
                c2_dict = {
                    "id": c2.id,
                    "name": c2.name,
                    "list": []
                }
                c1_dict['list'].append(c2_dict)
                for c3 in c2.sub_categories.all():
                    if not c3.active:
                        continue
                    c3_dict = {
                        "id": c3.id,
                        "name": c3.name
                    }
                    c2_dict['list'].append(c3_dict)
        cache.set('categories', res)
        result = res
    return {'status': 1, 'info': 'success', 'data': result}


def get_conditions(**kwargs):
    '''
        返回房间硬装检索条件
    '''
    label = ''
    if kwargs.get('label'):
        label = kwargs['label'][0]
    label_q = Q()
    if label:
        category = ProductCategory.objects.get(pk=label)
        if category.step == 1:
            label_q = Q(
                manufactory__categories__parent_category__parent_category=label)
        elif category.step == 2:
            label_q = Q(
                manufactory__categories__parent_category=label)
        elif category.step == 3:
            label_q = Q(
                manufactory__categories=label)
    brands_result = cache.get((label, 'brands'))
    if not brands_result:
        brands_array = []
        brands = ProductBrand.objects.filter(label_q, active=True)
        for brand in brands:
            brands_array.append({'id': brand.id, 'name': brand.name})
        cache.set((label, 'brands'), brands_array)
        brands_result = brands_array
    res = {'brand': brands_result, 'style': [
                    {'id':1,'name':'现代简约'},
                    {'id':2,'name':'中式'},
                    {'id':3,'name':'新中式'},
                    {'id':4,'name':'欧式'},
                    {'id':5,'name':'美式'},
                    {'id':6,'name':'北欧/宜家'},
                    {'id':7,'name':'地中海'},
                    {'id':8,'name':'东南亚'},
                    {'id':9,'name':'田园'},
                    {'id':10,'name':'新古典'},
                    {'id':11,'name':'明清古典'},
                    {'id':12,'name':'韩式'},
                    {'id':13,'name':'日式'},
                    {'id':14,'name':'其他'}
                    ], 'city': [], 'price': [],
           'sort': [{'type': 'category', 'name': u'分类'},
                    {'type': '-category', 'name': u'分类倒序'},
                    {'type': 'brand', 'name': u'品牌'},
                    {'type': '-brand', 'name': u'品牌倒序'},
                    {'type': 'series', 'name': u'系列'},
                    {'type': '-series', 'name': u'系列倒序'}
                    ]}
    return {'status': 1, 'info': 'success', 'data': res}


def get_series(**kwargs):
    '''
    返回品牌系列
    format:
    [{
"id": [int],
"name": [str]
      },]

    '''
    brand = kwargs.get('brand')
    if not brand:
        return {'status': 0, 'info': '参数brand不存在', 'data': []}
    brand = brand[0]
    series_array = cache.get((brand, 'series'))
    if not series_array:
        res = []
        series = ProductBrandSeries.objects.filter(brand=brand, active=True,
                                                   brand__active=True)
        for se in series:
            res.append({'id': se.id, 'name': se.name})
        cache.set((brand, 'series'), res)
        series_array = res
    return {'status': 1, 'info': 'success', 'data': series_array}


def get_model_data(**kwargs):
    '''
    返回家具模型的数据
    '''
    print kwargs
    page_size = 15
    if kwargs.get('pageSize'):
        page_size = kwargs['pageSize'][0]
    page = 1
    if kwargs.get('page'):
        page = kwargs['page'][0]
    label = 0
    if kwargs.get('label'):
        label = kwargs['label'][0]
    brand = 0
    if kwargs.get('Brand'):
        brand = kwargs['Brand'][0]
    series = 0
    if kwargs.get('Series'):
        series = kwargs['Series'][0]
    kw = ''
    if kwargs.get('kw'):
        kw = kwargs['kw'][0]
    sort = ''
    if kwargs.get('sort'):
        sort = kwargs['sort'][0]
    res = []
    category_q = Q()
    if label:
        category = ProductCategory.objects.filter(pk=label).first()
        if category:
            if category.step == 1:
                category_q = Q(category__parent_category__parent_category=category)
            elif category.step == 2:
                category_q = Q(category__parent_category=category)
            elif category.step == 3:
                category_q = Q(category=category)
    brand_q = Q()
    if brand:
        brand_q = Q(brand=brand)
    series_q = Q()
    if series:
        series_q = Q(series=series)
    kw_q = Q()
    if kw:
        kw_q = Q(name__icontains=kw) | Q(
            product_no__icontains=kw) | Q(
            category__parent_category__parent_category__name__icontains=kw) | Q(
            category__parent_category__name__icontains=kw) | Q(
            category__name__icontains=kw) | Q(
            manufactor__name__icontains=kw) | Q(
            brand__name__icontains=kw) | Q(
            series__name__icontains=kw)
    products = Product.objects.select_related('category',
                                              'category__parent_category',
                                              'category__parent_category__parent_category',
                                              'manufactor', 'brand',
                                              'series').prefetch_related(
        'models',
        'models__files').filter(kw_q,
                                category_q,
                                brand_q, series_q,
                                active=True, brand__isnull=False)
    if sort:
        products = products.order_by(sort)
    p = Paginator(products, page_size)
    page_data = p.page(page)
    for product in page_data.object_list:
        dingshi = ''
        faxian = ''
        tietu = ''
        tupian = ''
        gaomo = ''
        js = ''
        bin = ''
        for model in product.models.all():
            if not model.active:
                continue
            for file in model.files.all():
                if not file.active:
                    continue
                if model.source == 'kongjiandashi3D' and file.type == 'faxiantu':
                    faxian = settings.HOST + file.file.url
                if model.source == 'kongjiandashi3D' and file.type == 'tietu':
                    tietu = settings.HOST + file.file.url
                if model.source == 'kongjiandashi2D' and file.type == 'tupian':
                    dingshi = settings.HOST + file.file.url
                if model.source == 'chanpintupian' and file.type == 'tupian':
                    tupian = settings.HOST + file.file.url
                if file.type == 'js':
                    js = settings.HOST + file.file.url
                if file.type == 'bin':
                    bin = settings.HOST + file.file.url
        try:
            classify = '%s-%s-%s' % (
                product.category.parent_category.parent_category.name,
                product.category.parent_category.name, product.category.name)
        except Exception:
            classify = ''
        res.append({
            'id': product.id,
            'name': product.name,
            'brand': product.brand.name,
            'brandid': product.brand.id,
            'showImg': tupian,
            'floorplan': dingshi,
            'thumbImage': tupian,
            'uv_map': tietu,
            'm_uv_map': tietu,
            'normal_map': faxian,
            'm_normal_map': faxian,
            'bin': bin,
            'js': js,
            'size': '%sx%sx%s' % (
                product.length, product.width, product.height),
            'model': product.name,
            'price': product.price,
            'initialPrice': product.price,
            'classify': classify,
            'color': product.color,
            'style': '',
            'isCollect': True,
            'isNew': True,
            'isHot': True,
            'gm_path': gaomo
        })

    # todo
    return {'status': 1, 'info': 'success', 'data': res,
            'counts': products.count()}


def get_model_texture(**kwargs):
    '''
    返回家具模型的贴图
    format:
    [
    [{“map_uv”:[str], “map_fx”:[str]}, {..}],
    [{“map_uv”:[str], “map_fx”:[str]}]
    ]

    '''
    id = kwargs.get('id')
    if not id:
        return {'status': 0, 'info': '参数id不存在', 'data': []}
    id = id[0]
    product = Product.objects.filter(pk=id).first()
    if not product:
        return {'status': 0, 'info': '该商品不存在不存在', 'data': []}
    res = []
    for model in product.models.all():
        if not model.active:
            continue
        print model.source
        if model.source != 'kongjiandashi2D' and model.source != 'kongjiandashi3D':
            continue
        model_files = []
        tupian = ''
        faxian = ''
        for file in model.files.all():
            if not file.active:
                continue
            if file.type == 'faxiantu':
                faxian = settings.HOST + file.file.url
            if file.type == 'tietu':
                tupian = settings.HOST + file.file.url
        model_files.append({'map_uv': tupian, 'map_fx': faxian})
        res.append(model_files)
    # todo
    return {'status': 1, 'info': 'success', 'data': res}
