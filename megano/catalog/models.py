from django.db import models


def category_image_directory_path(instance: 'CategoryIcons', filename):
    """
    Получение пути для загрузки иконки категории
    :param instance: экземпляр класса
    :param filename: имя загружаемого файла
    :return: путь для загрузки файла
    """
    if instance.category.parent:
        return f'catalog/icons/{instance.category.parent}/{instance.category}/{filename}'
    else:
        return f'catalog/icons/{instance.category}/{filename}'


class Category(models.Model):
    """
    Модель категории
    """
    title = models.CharField(max_length=128, db_index=True, verbose_name='название')
    active = models.BooleanField(default=False, verbose_name='активная')
    parent = models.ForeignKey('self', on_delete=models.PROTECT, blank=True, null=True, related_name='subcategories',
                               verbose_name='родитель')
    favourite = models.BooleanField(default=False, verbose_name='избранная категория')

    class Meta:
        ordering = ["title", "pk"]
        verbose_name = "категория"
        verbose_name_plural = "категории"

    def href(self):
        """
        Получение ссылки
        :return: ссылка
        """
        return f'/catalog/{self.pk}'

    def __str__(self):
        return self.title


class CategoryIcons(models.Model):
    """
    Модель иконки категории
    """
    src = models.FileField(upload_to=category_image_directory_path, max_length=500, verbose_name='иконка')
    category = models.OneToOneField(Category, on_delete=models.CASCADE, related_name='image', verbose_name='категория',
                                    blank=True, null=True)

    class Meta:
        ordering = ["pk"]
        verbose_name = "иконка категории"
        verbose_name_plural = "иконки категорий"

    def alt(self):
        """
        Получение параметра 'alt' для отображения вместо иконки категории
        :return: название иконки
        """
        return self.category.title

    def __str__(self):
        return f'{self.pk}-я иконка'
