import sys
from PIL import Image

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.urls import reverse
from django.utils import timezone

from io import BytesIO


User = get_user_model()


def get_models_for_count(*model_names):
    return [models.Count(model_name) for model_name in model_names]


# 1 html tamplate for all products
def get_product_url(obj, view_name):
    ct_model = obj.__class__._meta.model_name
    return reverse(view_name, kwargs={'ct_model': ct_model, 'slug': obj.slug})


# Exeptions for resolutions
#class MinResolutionErrorException(Exception):
    #pass


#class MaxResolutionErrorException(Exception):
    #pass

#class for rendering all popular products on main page
class LatestProductsManager:

    @staticmethod
    def get_products_for_main_page(*args, **kwargs):
        with_respect_to = kwargs.get('with_respect_to')
        products = []
        ct_models = ContentType.objects.filter(model__in=args)
        for ct_model in ct_models:
            model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
            products.extend(model_products)
        if with_respect_to:
            ct_model = ContentType.objects.filter(model=with_respect_to)
            if ct_model.exists():
                if with_respect_to in args:
                    return sorted(products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True)
        return products


class LatestProducts:

    objects = LatestProductsManager()


class CategoryManager(models.Manager):

    CATEGORY_NAME_COUNT_NAME ={
        'Футболки': 'tshirt__count',
        'Сумки': 'bag__count',
        'Худі': 'hood__count',
        'Шопери': 'shoper__count',
        'Шкарпетки': 'sock__count',
        'Світшоти': 'sweetshot__count',
        'Штани/Джинси': 'pant__count',
        'Шарфи': 'scarf__count',
        'Куртки': 'jacket__count',
        'Патчі': 'patch__count',
    }

    def get_queryset(self):
        return super().get_queryset()

    def get_categories_for_left_sidebar(self):
        models = get_models_for_count('tshirt', 'bag', 'hood', 'shoper', 'sock', 'sweetshot', 'pant', 'scarf', 'jacket', 'patch')
        qs = list(self.get_queryset().annotate(*models))
        data = [
            dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
            for c in qs
        ]
        return data


class Category(models.Model):

    name = models.CharField(max_length=255, verbose_name='Назва категорії')
    slug = models.SlugField(unique=True)
    objects = CategoryManager()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category_detail', kwargs={'slug': self.slug})


class Product(models.Model):

    #values for validations with resolution and size of image
    # MIN_RESOLUTION = (400, 400)
    # MAX_RESOLUTION = (800, 800)
    # MAX_IMAGE_SIZE = 3145728

    class Meta:
        abstract = True

    category = models.ForeignKey(Category, verbose_name='Категорія', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, verbose_name='Найменування')
    slug = models.SlugField(unique=True)
    main_image = models.ImageField(verbose_name='Головне зображення')
    second_image = models.ImageField(verbose_name='Друге зображення')
    third_image = models.ImageField(verbose_name='Третьє зображення', blank=True, null=True)
    fourth_image = models.ImageField(verbose_name='Четверте зображення', blank=True, null=True)
    descriptions = models.TextField(verbose_name='Опис товару', blank=True, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=1, verbose_name='Ціна')

    def __str__(self):
        return self.title

    def get_model_name(self):
        return self.__class__.__name__.lower()

    # code to validate resolutions of image


    #     image = self.image
    #     img = Image.open(image)
    #     min_height, min_width = self.MIN_RESOLUTION
    #     max_height, max_width = self.MAX_RESOLUTION
    #     if img.height < min_height or img.width < min_width:
    #         raise MinResolutionErrorException('Розширення зображення меньше мінімального')
    #     if img.height > max_height or img.width > max_width:
    #         raise MaxResolutionErrorException('Розшірення зображення більше максимального')
    #     super().save(*args, **kwargs)


    # code for auto-cuting images resolution to 400 x 600
    def save(self, *args, **kwargs):
        main_image, second_image, third_image, fourth_image = self.main_image, \
                                                              self.second_image, \
                                                              self.third_image, \
                                                              self.fourth_image
        img1 = Image.open(main_image)
        img2 = Image.open(second_image)
        img3 = Image.open(third_image)
        img4 = Image.open(fourth_image)
        new_img1 = img1.convert('RGB')
        new_img2 = img2.convert('RGB')
        new_img3 = img3.convert('RGB')
        new_img4 = img4.convert('RGB')
        resized_new_img1 = new_img1.resize((400, 600), Image.ANTIALIAS)
        resized_new_img2 = new_img2.resize((400, 600), Image.ANTIALIAS)
        resized_new_img3 = new_img3.resize((400, 600), Image.ANTIALIAS)
        resized_new_img4 = new_img4.resize((400, 600), Image.ANTIALIAS)
        filestream1 = BytesIO()
        filestream2 = BytesIO()
        filestream3 = BytesIO()
        filestream4 = BytesIO()
        resized_new_img1.save(filestream1, 'JPEG', quality=90)
        resized_new_img2.save(filestream2, 'JPEG', quality=90)
        resized_new_img3.save(filestream3, 'JPEG', quality=90)
        resized_new_img4.save(filestream4, 'JPEG', quality=90)
        filestream1.seek(0)
        filestream2.seek(0)
        filestream3.seek(0)
        filestream4.seek(0)
        name1 = '{}.{}'.format(*self.main_image.name.split('.'))
        name2 = '{}.{}'.format(*self.second_image.name.split('.'))
        name3 = '{}.{}'.format(*self.third_image.name.split('.'))
        name4 = '{}.{}'.format(*self.fourth_image.name.split('.'))
        self.main_image = InMemoryUploadedFile(
            filestream1, 'ImageField', name1, 'jpeg/image', sys.getsizeof(filestream1), None
        )
        self.second_image = InMemoryUploadedFile(
            filestream2, 'ImageField', name2, 'jpeg/image', sys.getsizeof(filestream2), None
        )
        self.third_image = InMemoryUploadedFile(
            filestream3, 'ImageField', name3, 'jpeg/image', sys.getsizeof(filestream3), None
        )
        self.fourth_image = InMemoryUploadedFile(
            filestream4, 'ImageField', name4, 'jpeg/image', sys.getsizeof(filestream4), None
        )
        super().save(*args, **kwargs)


class TShirt(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')


    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Bag(Product):

    volume = models.CharField(max_length=255, verbose_name="Об'єм, л.", blank=True, null=True)

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Hood(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Shoper(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Sock(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Sweetshot(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Pant(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Scarf(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Jacket(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class Patch(Product):

    size = models.CharField(max_length=255, null=True, blank=True, verbose_name='Розмір')

    def __str__(self):
        return '{} : {}'.format(self.category.name, self.title)

    def get_absolute_url(self):
        return get_product_url(self, 'product_detail')


class CartProduct(models.Model):

    user = models.ForeignKey('Customer', verbose_name='Покупець', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Кошик', on_delete=models.CASCADE, related_name='related_products')
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    quantity = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Вартість')
    size = models.CharField(max_length=10, verbose_name='Розмір', blank=True, null=True)
    volume = models.CharField(max_length=10, verbose_name="Об'єм", blank=True, null=True)

    def __str__(self):
        return 'Продукт: {} (Для кошику)'.format(self.content_object.title)

    def save(self, *args, **kwargs):
        self.final_price = self.quantity * self.content_object.price
        super().save(*args, **kwargs)


class Cart(models.Model):

    owner = models.ForeignKey('Customer', null=True, verbose_name='Власник', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Загальна вартість')
    in_order = models.BooleanField(default=False)
    for_anonymus_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)


class Customer(models.Model):

    user = models.ForeignKey(User, verbose_name='Користувач', on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, verbose_name='Номер телефону', null=True, blank=True)
    address = models.CharField(max_length=255, verbose_name='Адреса', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Замовлення покупця', related_name='related_customer')

    def __str__(self):
        return 'Покупець: {} {}'.format(self.user.first_name, self.user.last_name)


class Order(models.Model):

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = {
        (STATUS_NEW, 'Нове замовлення'),
        (STATUS_IN_PROGRESS, 'Замовлення в розробці'),
        (STATUS_READY, 'Замовлення готове'),
        (STATUS_COMPLETED, 'Замовлення виконано')
    }

    BUYING_TYPE_CHOICES = {
        (BUYING_TYPE_SELF, 'Самовивіз, м. Одеса Преображенська 34'),
        (BUYING_TYPE_DELIVERY, 'Доставка'),

    }

    customer = models.ForeignKey(Customer, verbose_name='Покупець', related_name='related_orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255, verbose_name="Ім'я")
    last_name = models.CharField(max_length=255, verbose_name='Прізвище')
    phone = models.CharField(max_length=200, verbose_name='Телефон')
    mail = models.EmailField(max_length=30, verbose_name='E-mail', blank=True, null=True)
    cart = models.ForeignKey(Cart, verbose_name='Кошик', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=1024, verbose_name='Адреса', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус замовлення',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип замовлення',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_DELIVERY
    )
    comment = models.TextField(verbose_name='Коментар до замовлення', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата створення замовлення')


    def __str__(self):
        return str(self.id)
