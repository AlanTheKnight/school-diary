from __future__ import annotations

from io import BytesIO

from PIL import Image, ImageEnhance, ImageOps, UnidentifiedImageError
from django.core.files.base import ContentFile
from django.db import models

from apps.core.models import Users


class Category(models.Model):
    name = models.CharField("Название", max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class NotesGroup(models.Model):
    author = models.ForeignKey(Users, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория", null=True)
    upload_date = models.DateField("Дата загрузки", auto_now_add=True)
    title = models.CharField("Название", max_length=100)
    public = models.BooleanField("Виден ученикам из других классов", default=False)
    description = models.TextField("Описание", blank=True)

    class Meta:
        verbose_name = "Конспект"
        verbose_name_plural = "Конспекты"

    def __str__(self):
        return "{} (автор: {})".format(self.title, self.author.get_short_name())

    def files_size(self) -> int:
        size = 0
        for note in self.note_set.all():
            size += note.image.size
        return size

    def has_files(self):
        return self.note_set.filter(image__isnull=False).first() is not None

    def thumbnail(self):
        first = self.note_set.filter(image__isnull=False).first()
        if first is not None:
            return first.image
        return None

    def notes(self):
        return self.note_set.all()


def upload_notes(instance: Note, filename: str):
    return "notes/{}/{}".format(instance.group.id, filename)


class Note(models.Model):
    """
    Model that represents a single page in abstract.
    """
    group = models.ForeignKey(NotesGroup, on_delete=models.CASCADE, verbose_name="Группа")
    image = models.ImageField("Фото", upload_to=upload_notes)
    number = models.IntegerField("Номер", default=1)

    class Meta:
        verbose_name = "Страница"
        verbose_name_plural = "Страницы"

    def save(self, *args, enhance_image=False, **kwargs):
        try:
            img = Image.open(self.image)
        except UnidentifiedImageError:
            return False

        fmt = self.image.name.split(".")[-1]
        fmt = "JPEG" if fmt in ("jpg", "jpeg") else "PNG"

        # Resizes image and makes it's width maximum of 2000px
        max_width = 2000
        ratio = max_width / float(img.size[0])
        height = int(img.size[1] * ratio)
        img = img.resize((max_width, height))

        img = ImageOps.exif_transpose(img)

        # If enhance_image is True, it applies additional filters
        if enhance_image:
            img = ImageEnhance.Contrast(img).enhance(1.5)
            img = ImageEnhance.Brightness(img).enhance(1.2)
            img = ImageEnhance.Sharpness(img).enhance(1.2)
            img = ImageEnhance.Color(img).enhance(0.7)

        img_io = BytesIO()
        img.save(img_io, format=fmt, dpi=(400, 400))

        temp_name = self.image.name
        self.image.delete(save=False)

        self.image.save(
            temp_name,
            content=ContentFile(img_io.getvalue()),
            save=False
        )
        super(Note, self).save(*args, **kwargs)
        return True
