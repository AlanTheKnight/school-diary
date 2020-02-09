from django.db import models


class Publications(models.Model):
    publication_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата публикации")
    title = models.CharField(max_length=200, verbose_name="Название")
    content = models.TextField(max_length=5000, verbose_name="Текст")
    image = models.ImageField(upload_to='news/', verbose_name="Изображение", blank=True)
    slug = models.SlugField(max_length=100, verbose_name="Имя ссылки", unique=True)

    class Meta:
        ordering = ['-publication_date']
        verbose_name_plural = "Новости"
        verbose_name = "Новость"
    
    def __str__(self):
        return str(self.publication_date) + " " + self.title
        