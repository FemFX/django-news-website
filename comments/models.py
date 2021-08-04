from django.db import models
from news.models import News

# Create your models here.
class Comment(models.Model):
    author = models.CharField(max_length=50)
    text = models.CharField(max_length=250, verbose_name="Комментарий", default="")
    created_at = models.DateTimeField(auto_now_add=True)
    news_comments = models.ForeignKey(News, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ["-created_at"]
