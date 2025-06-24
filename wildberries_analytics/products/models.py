from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=500, verbose_name="Название товара")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена")
    sale_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Цена со скидкой")
    rating = models.FloatField(verbose_name="Рейтинг")
    reviews_count = models.IntegerField(verbose_name="Количество отзывов")
    query = models.CharField(max_length=255, verbose_name="Поисковый запрос")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    brand = models.CharField(max_length=255, blank=True, null=True, verbose_name="Бренд")
    product_id = models.CharField(max_length=50, blank=True, null=True, verbose_name="ID товара на WB")

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=['price']),
            models.Index(fields=['sale_price']),
            models.Index(fields=['rating']),
            models.Index(fields=['reviews_count']),
            models.Index(fields=['query']),
        ]
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} ({self.sale_price}₽)"

    @property
    def discount(self):
        """Рассчитывает размер скидки в процентах"""
        if self.price > 0 and self.sale_price < self.price:
            return round((1 - self.sale_price / self.price) * 100, 2)
        return 0

    @property
    def discount_amount(self):
        """Сумма скидки в рублях"""
        return self.price - self.sale_price if self.price > self.sale_price else 0