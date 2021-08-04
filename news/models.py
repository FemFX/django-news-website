from django.db import models
from django.urls import reverse

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=150, default="", verbose_name="Название")
    content = models.TextField(blank=True, verbose_name="Текст")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    photo = models.ImageField(
        blank=True, upload_to="photos/%Y/%m/%d/", verbose_name="Изображение"
    )
    is_published = models.BooleanField(default=True, verbose_name="Опубликовано")
    category = models.ForeignKey(
        "Category", on_delete=models.PROTECT, null=True, verbose_name="Категория"
    )

    def get_absolute_url(self):
        return reverse("getNews", kwargs={"news_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "News"
        verbose_name_plural = "News"
        ordering = ["-created_at"]


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True)

    def get_absolute_url(self):
        return reverse("getCategory", kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["-title"]


# cat = Category.objects.get(pk=1)
# news = cat.news_set.all()
