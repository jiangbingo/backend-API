# -*- encoding:utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from toolkits.tools import get_resources_path, utc2local, get_models_path


# 产品数据表
class Product(models.Model):
    TYPE_PRODUCT = 0
    TYPE_MODEL = 1
    TYPE_CHOICES = (
        (TYPE_PRODUCT, '产品'),
        (TYPE_MODEL, '模型'),
    )
    client_product_id = models.IntegerField(default=0, null=False)
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    category = models.ForeignKey('ProductCategory', related_name='products',
                                 default=None, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    brand = models.ForeignKey('ProductBrand', related_name='products',
                              default=None, null=True, blank=True,
                              on_delete=models.SET_NULL)
    series = models.ForeignKey('ProductBrandSeries', related_name='products',
                               default=None, null=True, blank=True,
                               on_delete=models.SET_NULL)
    # 产品编号
    product_no = models.CharField(max_length=200, default=None, null=True,
                                  blank=True)
    attr_val = models.CharField(max_length=100, default=None, null=True,
                                blank=True)
    rule_val = models.CharField(max_length=100, default=None, null=True,
                                blank=True)
    is_ornament = models.IntegerField(default=0, null=False)
    status = models.IntegerField(default=0, null=False)
    # 厂家
    manufactor = models.ForeignKey('Manufactor', related_name='products',
                                   default=None, null=True, blank=True,
                                   on_delete=models.SET_NULL)
    # 供应商
    distributors = models.ManyToManyField('Distributor',
                                          related_name='products',
                                          through='ProductDistributor')
    create_time = models.IntegerField(default=0, null=False)
    update_time = models.IntegerField(default=0, null=False)
    args = models.TextField(default='')
    # 备注
    remark = models.TextField(default='')
    type = models.IntegerField(default=TYPE_PRODUCT, choices=TYPE_CHOICES)
    version_no = models.CharField(max_length=200, default=None, null=True,
                                  blank=True)
    # 型号
    norms_no = models.CharField(max_length=200, default=None, null=True,
                                blank=True)
    # 材质
    material = models.CharField(max_length=100, default=None, null=True,
                                blank=True)
    # 长
    length = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    # 宽
    width = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    # 高
    height = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    # 工艺
    technics = models.CharField(max_length=100, default=None, null=True,
                                blank=True)
    # 颜色
    color = models.CharField(max_length=10, default=None, null=True, blank=True)
    # 价格
    price = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_product'

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.product_no)


class ProductAttribute(models.Model):
    product = models.ForeignKey("Product", related_name='attributes',
                                default=None,
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    attribute = models.ForeignKey('ProductCategoryAttribute', default=None,
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)
    value = models.CharField(max_length=200, null=True, blank=True,
                             default=None)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productattribute'

    def __unicode__(self):
        return '%s %s %s' % (
            self.product.name, self.attribute.name, self.value)


class ProductModelZip(models.Model):
    product = models.ForeignKey("Product", related_name='zip_files',
                                default=None,
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    file = models.FileField(upload_to=get_models_path(),
                            null=True, default=None)
    upload_time = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productmodelzip'


class ProductModel(models.Model):
    SOURCE_CHOICES = (
        'chanpintupian',
        'kongjiandashi2D',
        'kongjiandashi3D',
        'xuanran3D',
        'peishizushou',
        'IOS',
        'Android'
    )
    product = models.ForeignKey("Product", related_name='models', default=None,
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    # 来源
    source = models.CharField(max_length=200, null=True, blank=True,
                              default=None)
    # 规格
    size = models.CharField(max_length=200, null=True, blank=True,
                            default=None)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productmodel'


class ProductModelFiles(models.Model):
    TYPE_CHOICES = (
        'tupian',
        'moxing_obj',
        'moxing_mtl',
        'faxiantu',
        'tietu',
        'yinying',
        '3dmax'
    )
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    model = models.ForeignKey('ProductModel', related_name='files',
                              default=None,
                              null=True, blank=True,
                              on_delete=models.SET_NULL
                              )
    file = models.FileField(upload_to=get_models_path(),
                            null=True, default=None)
    type = models.CharField(max_length=200, null=True, blank=True,
                            default=None)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productmodelfiles'

    @property
    def file_name(self):
        regex = r'(\\|/)'
        import re
        file_name = re.split(regex, self.file.name)[-1]
        return file_name


class ProductModelPreviews(models.Model):
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    product = models.ForeignKey("Product", related_name='previews',
                                default=None,
                                null=True, blank=True,
                                on_delete=models.SET_NULL)
    file = models.FileField(upload_to=get_models_path(), null=True,
                            default=None)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productmodelpreviews'


class ProductDistributor(models.Model):
    product = models.ForeignKey("Product")
    distributor = models.ForeignKey("Distributor")
    link_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_productdistributor'


# 产品分类数据表
class ProductCategory(models.Model):
    parent_category = models.ForeignKey('ProductCategory',
                                        related_name='sub_categories',
                                        default=None, null=True, blank=True,
                                        on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    step = models.IntegerField(default=1, null=False)  # 分类目录树所处等级
    no = models.IntegerField(default=0, null=False)
    manufactors = models.ManyToManyField("Manufactor",
                                         through='CategoryManufactor',
                                         related_name='categories')
    active = models.BooleanField(default=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_productcategory"

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.category_no)

    @property
    def category_no(self):
        if self.step == 1:
            return 'a%s' % self.no
        elif self.step == 2:
            return 'b%s' % self.no
        else:
            return 'c%s' % self.no


class CategoryManufactor(models.Model):
    category = models.ForeignKey('ProductCategory')
    manufactor = models.ForeignKey('Manufactor')

    class Meta:
        db_table = 'products_categorymanufactor'


# 产品品牌关系数据
class ProductBrand(models.Model):
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    no = models.IntegerField(default=0, null=False)
    manufactory = models.ForeignKey('Manufactor', related_name='brands',
                                    default=None, null=True, blank=True,
                                    on_delete=models.SET_NULL
                                    )
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productbrand'

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.brand_no)

    @property
    def brand_no(self):
        return 'e%s' % self.no


# 产品品牌与系列关系数据表
class ProductBrandSeries(models.Model):
    brand = models.ForeignKey("ProductBrand", related_name='series',
                              default=None, null=True, blank=True,
                              on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, default=None, null=True, blank=True)
    no = models.IntegerField(default=0, null=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'products_productbrandseries'

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.series_no)

    @property
    def series_no(self):
        return 'f%s' % self.no


# 客户单位数据表
class Manufactor(models.Model):
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    no = models.IntegerField(default=0, null=False)
    # 厂商
    manufacturer = models.OneToOneField('CustomerAccount',
                                        related_name='manufactory',
                                        default=None, null=True, blank=True,
                                        on_delete=models.SET_NULL)
    # 拿到代理的经销商
    customers = models.ManyToManyField('CustomerAccount',
                                       related_name='manufactors',
                                       through='CustomerManufactor')
    # 注册号
    register_no = models.CharField(max_length=50, default=None, null=True,
                                   blank=True)
    # 营业执照
    business_license = models.FileField(default=None, null=True, blank=True,
                                        upload_to='business_license/')
    # 省
    province = models.CharField(max_length=200, default=None, null=True,
                                blank=True)
    # 市
    city = models.CharField(max_length=200, default=None, null=True,
                            blank=True)
    # 区
    area = models.CharField(max_length=200, default=None, null=True,
                            blank=True)
    # 联系人
    contact = models.CharField(max_length=200, default=None, null=True,
                               blank=True)
    # 联系电话
    contact_no = models.CharField(max_length=200, default=None, null=True,
                                  blank=True)
    image = models.ImageField(default=None, null=True, blank=True,
                              upload_to=get_resources_path())
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "products_manufactor"

    def __unicode__(self):
        return '%s(%s)' % (self.name, self.manufactor_no)

    @property
    def manufactor_no(self):
        return 'd%s' % self.no


# 产品分类属性关系数据表
class ProductCategoryAttribute(models.Model):
    STATUS_CHOICES = (
        (0, '未处理'),
        (1, '已处理')
    )
    category = models.ForeignKey("ProductCategory",
                                 related_name='attributes',
                                 default=None, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    name = models.CharField(max_length=100, default=None, null=True,
                            blank=True)
    searchable = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    # 来源
    source = models.CharField(max_length=200, default=None, null=True,
                              blank=True)
    # 状态
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_productcategoryattribute'

    def __unicode__(self):
        return self.name

    @property
    def value_string(self):
        values = []
        for value in self.values.all():
            if value.active:
                values.append(value.value)
        return ','.join(values)

    @property
    def value_dict(self):
        values = {}
        for value in self.values.all():
            if value.active:
                values.update({value.id: value.value})
        return values

    @property
    def value_array(self):
        values = []
        for value in self.values.all():
            if value.active:
                values.append(value.value)
        return values

    @property
    def status_unicode(self):
        return ProductCategoryAttribute.STATUS_CHOICES[self.status][1]

    @property
    def create_time(self):
        return self.create_date and utc2local(self.create_date).strftime(
            '%Y-%m-%d %H:%M:%S') or 'N/A'

    @property
    def update_time(self):
        return self.update_date and utc2local(self.update_date).strftime(
            '%Y-%m-%d %H:%M:%S') or 'N/A'


class ProductCategoryAttributeValue(models.Model):
    attribute = models.ForeignKey("ProductCategoryAttribute",
                                  related_name='values', default=None,
                                  null=True, blank=True,
                                  on_delete=models.SET_NULL)
    no = models.IntegerField(default=0)
    value = models.CharField(max_length=100, default=None, null=True,
                             blank=True)
    active = models.BooleanField(default=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'products_productcategoryattributevalue'

    def __unicode__(self):
        return '%s: %s' % (self.attribute.name, self.value)


class CustomerAccount(models.Model):
    SOURCE_MAIN = 0
    SOURCE_DESIGN = 1
    SOURCE_OR = 2
    SOURCE_SHOP = 3
    SOURCE_CHOICES = (
        (0, '官网'),
        (1, '设计师平台'),
        (2, '电商平台'),
        (3, '商铺')
    )

    ROLE_NORMAL = 0
    ROLE_DESIGNER = 1
    ROLE_OR = 2
    ROLE_SHOP = 3
    ROLE_DECORATION = 4
    ROLE_MANUFACTORY = 5
    ROLE_CHOICES = (
        (0, '普通用户'),
        (1, '设计师'),
        (2, '供应商'),
        (3, '供应商'),
        (4, '装修公司'),
        (5, '供应商')
    )

    GENDER_MALE = 0
    GENDER_FEMALE = 1
    GENDER_CHOICES = (
        (GENDER_MALE, '男'),
        (GENDER_FEMALE, '女'),
    )

    no = models.IntegerField(default=0)
    # 来源
    source = models.IntegerField(choices=SOURCE_CHOICES, default=SOURCE_MAIN)
    # 来源名称
    source_name = models.CharField(max_length=200, default=None, null=True,
                                   blank=True)
    # 用户名
    username = models.CharField(max_length=200, default=None, null=True,
                                blank=True)
    password = models.CharField(max_length=50, default=None, null=True,
                                blank=True)
    # 角色
    role = models.IntegerField(choices=ROLE_CHOICES, default=ROLE_NORMAL)
    # 状态
    active = models.BooleanField(default=True)
    # 注册日期
    register_date = models.DateTimeField(auto_now_add=True)
    # 头像
    avatar = models.ImageField(default=None, null=True, blank=True,
                               upload_to=get_resources_path())
    # 真实姓名
    real_name = models.CharField(max_length=200, default=None, null=True,
                                 blank=True)
    # 性别
    gender = models.IntegerField(choices=GENDER_CHOICES, default=GENDER_MALE)
    # 生日
    birth_date = models.DateField(default=None, null=True, blank=True)
    # 手机号码
    phone = models.CharField(max_length=50, default=None, null=True, blank=True)
    # 邮箱
    email = models.EmailField(max_length=200, default=None, null=True,
                              blank=True)
    email_certified = models.BooleanField(default=False)
    # 电话有效性认证
    phone_certified = models.BooleanField(default=False)
    # 认证
    certified = models.BooleanField(default=False)
    # 审核
    approved = models.BooleanField(default=False)

    class Meta:
        db_table = 'customers_customeraccount'

    def __unicode__(self):
        return '%s: %s' % (self.source_unicode, self.username)

    @property
    def role_unicode(self):
        return CustomerAccount.ROLE_CHOICES[self.role][1]

    @property
    def gender_unicode(self):
        return CustomerAccount.GENDER_CHOICES[self.gender][1]

    @property
    def customer_no(self):
        source = ''
        if self.source == 0:
            source = 'o'
        elif self.source == 1:
            source = 'd'
        elif self.source == 2:
            source = 'e'
        elif self.source == 3:
            source = 's'
        no = self.no
        for i in range(4 - len('%s' % self.no)):
            no = '0%s' % no
        role = ''
        if self.role == 0:
            role = 'n'
        elif self.role == 1:
            role = 'a'
        elif self.role == 2:
            role = 'e'
        elif self.role == 3:
            role = 's'
        elif self.role == 4:
            role = 'd'
        elif self.role == 5:
            role = 'm'
        return '%s%s%s%s' % (
            source, role, self.register_date.strftime('%Y%m%d'), no)

    @property
    def register_date_format(self):
        return self.register_date and utc2local(self.register_date).strftime(
            '%Y-%m-%d %H:%M:%S') or 'N/A'

    @property
    def source_unicode(self):
        if self.source_name:
            return self.source_name
        else:
            return CustomerAccount.SOURCE_CHOICES[self.source][1]


class AccountKey(models.Model):
    account = models.OneToOneField('CustomerAccount', related_name='key')
    token = models.CharField(max_length=128, unique=True, default='',
                             null=False)
    license = models.CharField(max_length=64, unique=True, default='',
                               null=False)
    app_secret = models.CharField(max_length=64, unique=True, default='',
                                  null=False)

    class Meta:
        db_table = 'customers_accountkey'

class OtherAccount(models.Model):
    """
        第三方用户表，商铺、电商的用户
    """
    platform = models.ForeignKey('CustomerAccount', related_name='other')
    platform_code = models.CharField(max_length=128, default='', null=False)
    username = models.CharField(max_length=128, default='', null=False)
    user_code = models.CharField(max_length=32, default='', null=False)

    class Meta:
        db_table = 'customers_otheraccount'

# 供应商
class Distributor(models.Model):
    # 供应商
    account = models.OneToOneField('CustomerAccount',
                                   related_name='distributor',
                                   default=None, null=True, blank=True,
                                   on_delete=models.SET_NULL)
    name = models.CharField(max_length=200, default=None, null=True,
                            blank=True)
    # 域名
    domain = models.CharField(max_length=200, default=None, null=True,
                              blank=True)
    # 公司名称
    company_name = models.CharField(max_length=200, default=None,
                                    null=True,
                                    blank=True)
    # 描述
    description = models.CharField(max_length=2000, default=None,
                                   null=True,
                                   blank=True)
    # 注册号
    register_no = models.CharField(max_length=50, default=None,
                                   null=True,
                                   blank=True)
    # 身份信息
    cert_no = models.CharField(max_length=50, default=None, null=True,
                               blank=True)
    # 银行帐号
    bank_no = models.CharField(max_length=50, default=None, null=True,
                               blank=True)
    # 营业执照
    business_license = models.FileField(default=None, null=True,
                                        blank=True,
                                        upload_to=get_resources_path())
    brands = models.ManyToManyField('ProductBrand',
                                    through='DistributorBrand',
                                    related_name='distributors')
    designers = models.ManyToManyField('Designer',
                                       related_name='designer_distributors',
                                       through='DesignerDistributor')

    class Meta:
        db_table = 'customers_distributor'

    def __unicode__(self):
        return '%s' % self.name


class DistributorBrand(models.Model):
    distributor = models.ForeignKey('Distributor')
    brand = models.ForeignKey('ProductBrand')

    class Meta:
        db_table = 'products_distributorbrand'


# 设计师
class Designer(models.Model):
    account = models.OneToOneField('CustomerAccount',
                                   related_name='designer',
                                   default=None, null=True, blank=True,
                                   on_delete=models.SET_NULL)
    # 身份信息
    cert_no = models.CharField(max_length=50, default=None, null=True,
                               blank=True)
    # 社交帐号
    social_account = models.CharField(max_length=50, default=None,
                                      null=True,
                                      blank=True)
    # 所在地
    location = models.CharField(max_length=200, default=None, null=True,
                                blank=True)
    # 公司名称
    company_name = models.CharField(max_length=200, default=None, null=True,
                                    blank=True)
    # 公司地址
    company_address = models.CharField(max_length=200, default=None,
                                       null=True,
                                       blank=True)
    # 设计风格
    design_style = models.CharField(max_length=200, default=None, null=True,
                                    blank=True)
    # 个人简介
    personal_profile = models.CharField(max_length=500, default=None,
                                        null=True,
                                        blank=True)
    # 身份证附件正面
    cert_attachment_front = models.ImageField(default=None, null=True,
                                              blank=True,
                                              upload_to=get_resources_path())
    # 身份证附件背面
    cert_attachment_back = models.ImageField(default=None, null=True,
                                             blank=True,
                                             upload_to=get_resources_path())
    # 设计师资格证正面
    designer_cert_front = models.ImageField(default=None, null=True,
                                            blank=True,
                                            upload_to=get_resources_path())
    # 设计师资格证背面
    designer_cert_back = models.ImageField(default=None, null=True,
                                           blank=True,
                                           upload_to=get_resources_path())

    class Meta:
        db_table = 'customers_designer'

    def __unicode__(self):
        return '%s' % self.name


class DesignerDistributor(models.Model):
    designer = models.ForeignKey('Designer')
    distributor = models.ForeignKey('Distributor')

    class Meta:
        db_table = 'customers_designerdistributor'


class CustomerManufactor(models.Model):
    customer = models.ForeignKey('CustomerAccount')
    manufactor = models.ForeignKey('Manufactor')

    class Meta:
        db_table = 'products_customermanufactor'


class Province(models.Model):
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    fullname = models.CharField(max_length=50, default=None, blank=True,
                                null=True)
    area_code = models.IntegerField(default=0)
    pinyin = models.CharField(max_length=50, default=None, blank=True,
                              null=True)
    location_lat = models.DecimalField(max_digits=20, decimal_places=10)
    location_lng = models.DecimalField(max_digits=20, decimal_places=10)

    class Meta:
        db_table = 'property_province'

    def __unicode__(self):
        return self.fullname


class City(models.Model):
    province = models.ForeignKey('Province', related_name='cities')
    name = models.CharField(max_length=50, default=None, blank=True, null=True)
    fullname = models.CharField(max_length=50, default=None, blank=True,
                                null=True)
    area_code = models.IntegerField(default=0)
    pinyin = models.CharField(max_length=50, default=None, blank=True,
                              null=True)
    location_lat = models.DecimalField(max_digits=20, decimal_places=10)
    location_lng = models.DecimalField(max_digits=20, decimal_places=10)
    post_code = models.CharField(max_length=50, default=None, blank=True,
                                 null=True)
    phone_code = models.CharField(max_length=50, default=None, blank=True,
                                  null=True)

    def __unicode__(self):
        return self.fullname

    class Meta:
        db_table = 'property_city'


class Area(models.Model):
    city = models.ForeignKey('City', related_name='areas')
    fullname = models.CharField(max_length=50, default=None, blank=True,
                                null=True)
    area_code = models.IntegerField(default=0)
    location_lat = models.DecimalField(max_digits=20, decimal_places=10)
    location_lng = models.DecimalField(max_digits=20, decimal_places=10)

    def __unicode__(self):
        return self.fullname

    class Meta:
        db_table = 'property_area'

# 楼盘数据表
class Property(models.Model):
    TYPE_RESIDENCE = 0
    TYPE_COMMERCIAL = 1
    TYPE_INDUSTRY = 2
    TYPE_ADMINISTRATION = 3
    TYPE_PUBLIC = 4
    TYPE_CHOICES = (
        (TYPE_RESIDENCE, '住宅'),
        (TYPE_COMMERCIAL, '商业'),
        (TYPE_INDUSTRY, '工业'),
        (TYPE_ADMINISTRATION, '行政、事业单位'),
        (TYPE_PUBLIC, '公益')
    )

    STATUS_CHOICES = (
        (0, '地块'),
        (1, '开工'),
        (2, '售楼处开放'),
        (3, '排号'),
        (4, '选房'),
        (5, '开盘'),
        (6, '顺销'),
        (7, '售罄'),
        (8, '交房')
    )

    # 编号
    no = models.CharField(max_length=200, default=None, null=True, blank=True)
    # 名称
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    # 地址
    address = models.CharField(max_length=200, default=None, null=True,
                               blank=True)
    # 省
    province = models.ForeignKey('Province', related_name='properties',
                                 default=None, null=True, blank=True,
                                 on_delete=models.SET_NULL)
    # 市
    city = models.ForeignKey('City', related_name='properties', default=None,
                             null=True, blank=True, on_delete=models.SET_NULL)
    # 区
    area = models.ForeignKey('Area', related_name='properties', default=None,
                             null=True, blank=True, on_delete=models.SET_NULL)
    # 开发商
    develop_manufactor = models.CharField(max_length=300, default=None,
                                          null=True, blank=True)
    # 产权年限
    property_right_limit = models.IntegerField(default=0)
    # 物业类型
    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_RESIDENCE)
    # 均价
    avg_price = models.DecimalField(max_digits=20, decimal_places=2)
    # 状态
    status = models.IntegerField(choices=STATUS_CHOICES, default=0)
    # 容积率
    volume_ratio = models.DecimalField(max_digits=4, decimal_places=2)
    # 开盘时间
    open_time = models.DateField(null=True, blank=True, default=None)
    # 绿化率
    greening_rate = models.DecimalField(max_digits=4, decimal_places=2)
    # 物业公司
    property_manufactor = models.CharField(max_length=200, default=None,
                                           blank=True,
                                           null=True)
    # 交房时间
    deliver_date = models.DateField(null=True, blank=True, default=None)
    # 建筑类型
    build_type = models.CharField(max_length=200, default=None, blank=True,
                                  null=True)
    # 物业费
    property_price = models.DecimalField(max_digits=20, decimal_places=2)
    # 车位数
    parking_count = models.IntegerField(default=0)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'property_property'

    tag_attr_map = {
        u'开发商': 'develop_manufactor',
        u'产权年限': 'property_right_limit',
        u'物业类型': 'type',
        u'均价': 'avg_price',
        u'楼盘状态': 'status',
        u'容积率': 'volume_ratio',
        u'开盘时间': 'open_time',
        u'绿化率': 'greening_rate',
        u'交房时间': 'deliver_date',
        u'建筑类型': 'build_type',
        u'物业费': 'property_price',
        u'车位数': 'parking_count'
    }

    @property
    def status_unicode(self):
        return Property.STATUS_CHOICES[self.status][1]

    @property
    def type_unicode(self):
        return Property.TYPE_CHOICES[self.type][1]

    def time_format(self):
        if not self.create_time and not self.update_time:
            return '0000-00-00 00:00:00'
        elif self.create_time and not self.update_time:
            return utc2local(self.create_time).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return utc2local(self.update_time).strftime('%Y-%m-%d %H:%M:%S')

    def active_apartments(self):
        return self.apartments.filter(active=True)

    def tag_args(self):
        tags = []
        labels = Label.objects.prefetch_related('values').filter(active=True)
        for label in labels:
            tag_name = label.name
            label_values = []
            for value in label.values.all():
                if not value.active:
                    continue
                if value.value:
                    label_values.append(value.value)
            if self.tag_attr_map.get(tag_name):
                tags.append(
                    {'name': tag_name, 'value': self.get_attr(tag_name), 'choices':label_values, 'data-for':self.tag_attr_map[tag_name],'type':label.label_type})
            else:
                tags.append(
                    {'name': tag_name, 'value': self.get_attr(tag_name),
                     'choices': label_values,
                     'data-for': tag_name,'type':label.label_type})
        return tags

    def save_attr(self, args):
        tags = []
        tag_names = [tag.name for tag in Label.objects.filter(active=True)]
        for key,value in args.items():
            if not self.tag_attr_map.get(key):
                if key in tag_names:
                    if self.id:
                        property_tag,flag = PropertyTag.objects.get_or_create(property=self,name=key)
                        property_tag.value = value
                        property_tag.save()
                    else:
                        property_tag = PropertyTag(property=self,name=key,value=value)
                        tags.append(property_tag)
        self.save()
        if tags:
            PropertyTag.objects.bulk_create(tags)

    def get_attr(self, attr_name):
        value = 'N/A'
        if self.tag_attr_map.get(attr_name):
            value = getattr(self, self.tag_attr_map[attr_name])
        else:
            for tag in self.tags.all():
                print tag.name,attr_name
                if tag.name == attr_name:
                    value = tag.value
                    break
        return value

class PropertyTag(models.Model):
    property = models.ForeignKey('Property', related_name='tags')
    name = models.CharField(max_length=200, null=True, blank=True,
                            default=None)
    value = models.CharField(max_length=200, null=True, blank=True,
                             default=None)

    class Meta:
        db_table = 'property_propertytag'


class Apartment(models.Model):
    ORIENTATION_SOUTH = 0
    ORIENTATION_NORTH = 1
    ORIENTATION_EAST = 2
    ORIENTATION_WEST = 3
    ORIENTATION_EASTSOUTH = 4
    ORIENTATION_EASTNORTH = 5
    ORIENTATION_WESTNORTH = 6
    ORIENTATION_WESTSOUTH = 7
    ORIENTATION_CHOICES = (
        (ORIENTATION_SOUTH, '南'),
        (ORIENTATION_NORTH, '北'),
        (ORIENTATION_EAST, '东'),
        (ORIENTATION_WEST, '西'),
        (ORIENTATION_EASTSOUTH, '东南'),
        (ORIENTATION_EASTNORTH, '东北'),
        (ORIENTATION_WESTNORTH, '西北'),
        (ORIENTATION_WESTSOUTH, '西南')
    )

    property = models.ForeignKey('Property', related_name='apartments')
    # 编号
    no = models.IntegerField(default=0)
    # 户型编号
    apartment_no = models.CharField(max_length=200, default=None, null=True,
                                    blank=True)
    # 户型名称
    name = models.CharField(max_length=200, default=None, null=True, blank=True)
    # 面积
    acreage = models.DecimalField(max_digits=20, decimal_places=2)
    # 室
    room_count = models.IntegerField(default=0)
    # 厅
    hall_count = models.IntegerField(default=0)
    # 厨
    kitchen_count = models.IntegerField(default=0)
    # 卫
    restroom_count = models.IntegerField(default=0)
    # 层高
    height = models.DecimalField(max_digits=4, decimal_places=2)
    # 朝向
    orientation = models.IntegerField(choices=ORIENTATION_CHOICES,
                                      default=ORIENTATION_SOUTH)
    # 卧室描述
    room_description = models.CharField(max_length=500, default=None, null=True)
    # 客厅描述
    living_room_description = models.CharField(max_length=500, default=None,
                                               null=True)
    # 餐厅描述
    dining_room_description = models.CharField(max_length=500, default=None,
                                               null=True)
    # 卫生间描述
    restroom_description = models.CharField(max_length=500, default=None,
                                            null=True)
    # 花园描述
    garden_description = models.CharField(max_length=500, default=None,
                                          null=True)
    # 其他描述
    other_description = models.CharField(max_length=500, default=None,
                                         null=True)
    # 户型图
    preview = models.ImageField(upload_to=get_resources_path(), default=None,
                                null=True)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def orientation_unicode(self):
        return Apartment.ORIENTATION_CHOICES[self.orientation][1]

    def time_format(self):
        if not self.create_time and not self.update_time:
            return '0000-00-00 00:00:00'
        elif self.create_time and not self.update_time:
            return utc2local(self.create_time).strftime('%Y-%m-%d %H:%M:%S')
        else:
            return utc2local(self.update_time).strftime('%Y-%m-%d %H:%M:%S')

    class Meta:
        db_table = 'property_apartment'


class Label(models.Model):
    TYPE_CHOICES = (
        (0, '标签值'),
        (1, '标签范围')
    )
    name = models.CharField(max_length=200, null=True, blank=True,
                            default=None)
    active = models.BooleanField(default=True)
    label_type = models.IntegerField(choices=TYPE_CHOICES, default=0)

    def __unicode__(self):
        return self.name

    class Meta:
        db_table = 'property_label'

    @property
    def top_line_values(self):
        return self.active_values[:8]

    @property
    def has_other_line(self):
        if len(self.active_values) > 8:
            return True
        else:
            return False

    @property
    def other_line_values(self):
        result = []
        count = len(self.active_values)
        if count <= 8:
            return result
        line = (count - 8) / 8 + 1
        for line_no in range(line):
            values = self.active_values[8 * line_no + 8:8 * line_no + 16]
            result.append(values)
        return result

    @property
    def active_values(self):
        result = []
        for value in self.values.all():
            if value.active:
                result.append(value)
        return result


class LabelValue(models.Model):
    label = models.ForeignKey('Label', related_name='values')
    value_min = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    value_max = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    value = models.CharField(max_length=200, null=True, blank=True,
                             default=None)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'property_labelvalue'

    def __unicode__(self):
        if self.label.label_type:
            return '%s ~ %s' % (self.value_min % 1 == 0 and int(self.value_min) or float(self.value_min), self.value_max % 1 == 0 and int(self.value_max) or float(self.value_max))
        else:
            return '%s' % (self.value or '')


class Macro(models.Model):
    TYPE_BRICK = 0
    TYPE_LINE = 1
    TYPE_PARQUET = 2
    TYPE_WALL = 3
    TYPE_ROOM = 4
    TYPE_CHOICES = (
        (TYPE_BRICK,'造型砖'),
        (TYPE_LINE,'腰线框、波打线'),
        (TYPE_PARQUET,'拼花'),
        (TYPE_WALL,'墙面装修'),
        (TYPE_ROOM,'样板间')
    )
    type = models.IntegerField(default=TYPE_BRICK,choices=TYPE_CHOICES)
    # 用户
    account = models.ForeignKey('CustomerAccount',
                                related_name='macros',
                                default=None, null=True, blank=True,
                                on_delete=models.SET_NULL)
    # 商铺或电商的客户
    other_account = models.ForeignKey('OtherAccount',
                                      related_name='macros',
                                      default=None, null=True, blank=True,
                                      on_delete=models.SET_NULL)
    paving_id = models.IntegerField(default=0)
    paving_name = models.CharField(max_length=200, default=None, null=True, blank=True)
    cnf_type = models.CharField(max_length=200, default=None, null=True, blank=True)
    cnf_name = models.CharField(max_length=200, default=None, null=True, blank=True)
    style_id = models.IntegerField(default=0)
    brands = models.ManyToManyField('ProductBrand',related_name='macros',through='MacroBrand')
    suitable_material = models.CharField(max_length=200, default=None, null=True, blank=True)
    cnf_body = models.FileField(upload_to=get_resources_path(),default=None,blank=True,null=True)
    img = models.ImageField(upload_to=get_resources_path(), default=None,
                                blank=True, null=True)
    edge = models.IntegerField(default=1)
    is_share = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'scheme_macro'

class MacroBrand(models.Model):
    brand = models.ForeignKey('ProductBrand')
    macro = models.ForeignKey('Macro')

    class Meta:
        db_table = 'scheme_macrobrand'