from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, verbose_name='Производитель')
    slug = models.SlugField()
    country = models.CharField(max_length=100, verbose_name='Страна производитель')

    class Meta:
        verbose_name = 'Производитель'
        verbose_name_plural = 'Производители'

    def __str__(self):
        return f"{self.name} | {self.country}"


class Season(models.Model):
    name = models.CharField(max_length=255, verbose_name='Сезон одежды')

    class Meta:
        verbose_name = 'Сезон'
        verbose_name_plural = 'Сезоны'

    def __str__(self):
        return self.name


class Products(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование товара')
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name='Производитель')
    season = models.ForeignKey(Season, on_delete=models.CASCADE, verbose_name='Сезон одежды')
    price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Цена товара')
    description = models.TextField(verbose_name='Описание')
    slug = models.SlugField()
    stock = models.IntegerField(default=1, verbose_name='Наличие на складе')
    offer_of_the_week = models.BooleanField(default=False, verbose_name='Предложение недели ')
    release_date = models.DateField(verbose_name='Дата выпуса')

    def __str__(self):
        return f"{self.id} | {self.name} | {self.manufacturer.name} | {self.season.name}"

    @property
    def ct_model(self):
        return self._meta.model_name

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class CartProduct(models.Model):
    user = models.ForeignKey('Customer', verbose_name='Покупатель', on_delete=models.CASCADE)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    object_id = models.PositiveIntegerField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1, verbose_name='Количество товара')

    def __str__(self):
        return f"Продукт: {self.content_object.name}(для корзины)"

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.content_object.price
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Товар для корзины'
        verbose_name_plural = 'Товары для корзины'


class Cart(models.Model):
    owner = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    products = models.ManyToManyField(
        CartProduct, blank=True, null=True, related_name='related_cart', verbose_name='Продукты для корзины'
    )
    total_products = models.IntegerField(default=0, verbose_name='Общее количество товара')
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class Order(models.Model):
    """Заказы покупателя"""

    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICE = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ отдан')
    )

    BUYING_TYPE_CHOICE = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey('Customer', on_delete=models.CASCADE, verbose_name='Покупатель')
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    phone = models.CharField(max_length=20, verbose_name='Номер телефона')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    status = models.CharField(max_length=100, choices=STATUS_CHOICE, default=STATUS_NEW, verbose_name='Статус заказа')
    buying_type = models.CharField(max_length=100, choices=BUYING_TYPE_CHOICE, default=BUYING_TYPE_SELF, verbose_name='Тип заказа')



